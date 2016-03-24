

def finddialogbetween(u1id, u2id):
    q1 = Dialog.query.filter(Dialog.user1_id == u1id).filter(Dialog.user2_id == u2id)
    q2 = Dialog.query.filter(Dialog.user1_id == u2id).filter(Dialog.user2_id == u1id)
    return q1.union(q2)