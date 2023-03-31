from charm.toolbox.pairinggroup import G1, G2, pair, ZR
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.ABEnc import ABEnc

debug = False


class CPabe09(ABEnc):

    def __init__(self, groupObj):
        ABEnc.__init__(self)
        global util, group
        util = SecretUtil(groupObj, debug)
        group = groupObj

    def setup(self, g1 = None, g2 = None, alpha = None, a = None):
        if not (g1 is None or g2 is None or alpha is None or a is None):
            print("case 1")
            g1 = group.deserialize(g1)
            g2 = group.deserialize(g2)
            print("hi")
            alpha = group.deserialize(alpha)
            a = group.deserialize(a)
        else:
            print("case 2")
            g1, g2 = group.random(G1), group.random(G2)
            alpha, a = group.random(), group.random()

        e_gg_alpha = pair(g1, g2) ** alpha
        msk = {'g1^alpha': g1 ** alpha, 'g2^alpha': g2 ** alpha}
        pk = {'g1': g1, 'g2': g2, 'e(gg)^alpha': e_gg_alpha, 'g1^a': g1 ** a, 'g2^a': g2 ** a}
        return msk, pk
        # return g1, g2, alpha, a

    def keygen(self, pk, msk, attributes):
        t = group.random()
        K = msk['g2^alpha'] * (pk['g2^a'] ** t)
        L = pk['g2'] ** t
        k_x = [group.hash(s, G1) ** t for s in attributes]

        K_x = {}
        for i in range(0, len(k_x)):
            K_x[attributes[i]] = k_x[i]

        key = {'K': K, 'L': L, 'K_x': K_x, 'attributes': attributes}
        return key

    def encrypt(self, pk, M, policy_str):
        # Extract the attributes as a list
        policy = util.createPolicy(policy_str)
        p_list = util.getAttributeList(policy)
        s = group.random()
        C_tilde = (pk['e(gg)^alpha'] ** s) * M
        C_0 = pk['g1'] ** s
        C, D = {}, {}
        secret = s
        shares = util.calculateSharesList(secret, policy)

        # ciphertext
        for i in range(len(p_list)):
            r = group.random()
            if shares[i][0] == p_list[i]:
                attr = shares[i][0].getAttribute()
                C[p_list[i]] = ((pk['g1^a'] ** shares[i][1])
                                * (group.hash(attr, G1) ** -r))
                D[p_list[i]] = (pk['g2'] ** r)

        if debug:
            print("SessionKey: %s" % C_tilde)
        return {'C0': C_0, 'C': C, 'D': D, 'C_tilde': C_tilde, 'policy': policy_str, 'attribute': p_list}

    def decrypt(self, pk, sk, ct):
        policy = util.createPolicy(ct['policy'])
        pruned = util.prune(policy, sk['attributes'])
        if pruned == False:
            return False
        coeffs = util.getCoefficients(policy)
        numerator = pair(ct['C0'], sk['K'])

        # create list for attributes in order...
        k_x, w_i = {}, {}
        for i in pruned:
            j = i.getAttributeAndIndex()
            k = i.getAttribute()
            k_x[j] = sk['K_x'][k]
            w_i[j] = coeffs[j]
            # print('Attribute %s: coeff=%s, k_x=%s' % (j, w_i[j], k_x[j]))

        C, D = ct['C'], ct['D']
        denominator = 1
        for i in pruned:
            j = i.getAttributeAndIndex()
            denominator *= (pair(C[j] ** w_i[j], sk['L'])
                            * pair(k_x[j] ** w_i[j], D[j]))
        return ct['C_tilde'] / (numerator / denominator)
