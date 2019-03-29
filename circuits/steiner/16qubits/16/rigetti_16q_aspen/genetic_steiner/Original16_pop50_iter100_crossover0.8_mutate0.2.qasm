// Initial wiring: [7, 2, 8, 5, 3, 9, 6, 15, 0, 1, 12, 11, 10, 13, 14, 4]
// Resulting wiring: [7, 2, 8, 5, 3, 9, 6, 15, 0, 1, 12, 11, 10, 13, 14, 4]
OPENQASM 2.0;
include "qelib1.inc";
qreg q[16];
cx q[6], q[5];
cx q[7], q[6];
cx q[6], q[5];
cx q[5], q[4];
cx q[6], q[5];
cx q[9], q[8];
cx q[13], q[12];
cx q[14], q[13];
cx q[15], q[14];
cx q[15], q[8];
cx q[14], q[15];
cx q[12], q[13];
cx q[10], q[11];
cx q[9], q[10];
cx q[10], q[11];
cx q[11], q[12];
cx q[12], q[13];
cx q[13], q[14];
cx q[14], q[15];
cx q[11], q[10];
cx q[13], q[12];
cx q[15], q[14];
cx q[7], q[8];
cx q[8], q[15];
cx q[8], q[9];
cx q[6], q[7];
cx q[7], q[8];
cx q[8], q[15];
cx q[8], q[9];
cx q[7], q[6];
cx q[15], q[8];
cx q[5], q[6];
cx q[6], q[7];
cx q[7], q[6];
cx q[0], q[15];
cx q[15], q[8];