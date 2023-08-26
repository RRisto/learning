q0->qAppZero: x;S
qAppZero->q1: x;R
q1->q1: TGA;y,R
q1->q2: x;L
q1->q3: C;y,R
q2->q2: y;L
q2->qDel: x;S
qDel->qH: x;S
q3->q3: !x;R
q3->qIncr: x;S
qIncr->q4: x;S
q4->q4: !y;L
q4->q1: y;R

block: qAppZero=appendZero.tm
block: qDel=deleteToInteger.tm
block: qIncr=incrementWithOverflow.tm

