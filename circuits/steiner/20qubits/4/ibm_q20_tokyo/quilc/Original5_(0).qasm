// EXPECTED_REWIRING [0 1 2 3 4 5 12 7 8 9 10 6 11 13 14 15 16 17 18 19]
// CURRENT_REWIRING [0 1 2 3 4 5 12 7 8 9 10 6 17 13 14 15 16 11 18 19]
OPENQASM 2.0;
include "qelib1.inc";
qreg q[20];
rz(-1.5707963267948966*pi) q[8];
rx(1.5707963267948966*pi) q[8];
cz q[8], q[10];
rz(-1.7843290499389812*pi) q[17];
rx(1.5707963267948966*pi) q[17];
rz(2.077989633526896*pi) q[17];
rx(-1.5707963267948966*pi) q[17];
rz(-0.8103884456122044*pi) q[17];
rx(-1.5707963267948966*pi) q[8];
rz(-1.5707963267948966*pi) q[11];
rx(1.5707963267948966*pi) q[11];
cz q[11], q[8];
rz(1.674236967864048*pi) q[11];
rx(1.5707963267948966*pi) q[11];
rz(1.4189783790674746*pi) q[11];
rx(-1.5707963267948966*pi) q[11];
cz q[17], q[11];
rz(1.6366529270088535*pi) q[11];
rx(1.5707963267948966*pi) q[11];
rz(-1.5707963267948966*pi) q[17];
rx(-1.5707963267948966*pi) q[17];
cz q[17], q[11];
rx(-1.5707963267948966*pi) q[11];
rx(1.5707963267948966*pi) q[17];
cz q[17], q[11];
rz(3.141592653589793*pi) q[8];
rx(1.5707963267948966*pi) q[8];
rz(-0.6542456812873576*pi) q[11];
rx(1.5707963267948966*pi) q[11];
rz(0.9242262418970197*pi) q[11];
rx(-1.5707963267948966*pi) q[11];
cz q[8], q[11];
rz(-1.5707963267948966*pi) q[6];
rx(1.5707963267948966*pi) q[6];
cz q[6], q[4];
rz(3.141592653589793*pi) q[4];
rx(-1.5707963267948966*pi) q[6];
rz(1.5707963267948966*pi) q[6];
rx(-1.5707963267948966*pi) q[8];
rz(1.5707963267948966*pi) q[8];
rz(3.141592653589793*pi) q[10];
rz(0.6463506146747173*pi) q[11];
rz(1.4564375502462918*pi) q[17];
rx(1.5707963267948966*pi) q[17];
rz(1.426995486693993*pi) q[17];
rx(-1.5707963267948966*pi) q[17];
rz(-3.059616298134544*pi) q[17];