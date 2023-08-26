# This is the version of containsGAGA used in chapter 10 for
# experimenting with running times of Turing machines.
q0->q0: CAT;R
q0->q1:   G;R
q0->qR:   _;S
q1->q2:   A;R
q1->q0:  CT;R
q1->q1:   G;R
q1->qR:   _;S
q2->q3:   G;R
q2->q0: CAT;R
q2->qR:   _;S
q3->qA:   A;R
q3->q0:  CT;R
q3->q1:   G;R
q3->qR:   _;S
