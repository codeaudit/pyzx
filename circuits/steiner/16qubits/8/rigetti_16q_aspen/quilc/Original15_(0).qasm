// EXPECTED_REWIRING [12 2 1 4 3 5 6 7 8 10 9 11 14 15 0 13]
// CURRENT_REWIRING [12 1 0 4 2 5 6 7 8 10 9 11 14 3 15 13]
OPENQASM 2.0;
include "qelib1.inc";
qreg q[16];
rz(-1.5707963267948966*pi) q[11];
rx(1.5707963267948966*pi) q[11];
cz q[11], q[12];
rz(-1.5707963267948966*pi) q[0];
rx(1.5707963267948966*pi) q[0];
cz q[0], q[1];
rz(-0.6641532911097666*pi) q[0];
rx(1.5707963267948966*pi) q[0];
rz(2.1124377966214545*pi) q[0];
rx(-1.5707963267948966*pi) q[0];
rz(-0.5382013906098936*pi) q[0];
rz(0.8795405612495313*pi) q[15];
rx(1.5707963267948966*pi) q[15];
rz(0.7286495265185148*pi) q[15];
rx(-1.5707963267948966*pi) q[15];
cz q[0], q[15];
rx(-1.5707963267948966*pi) q[0];
rz(2.8047282907819673*pi) q[15];
rx(1.5707963267948966*pi) q[15];
cz q[0], q[15];
rx(1.5707963267948966*pi) q[0];
rx(-1.5707963267948966*pi) q[15];
cz q[0], q[15];
rz(-1.7843290499389812*pi) q[2];
rx(1.5707963267948966*pi) q[2];
rz(2.077989633526896*pi) q[2];
rx(-1.5707963267948966*pi) q[2];
rz(-0.8103884456122044*pi) q[2];
rz(-2.395742606506989*pi) q[0];
rx(1.5707963267948966*pi) q[0];
rz(1.0322960541721458*pi) q[0];
rx(-1.5707963267948966*pi) q[0];
rz(-2.013271884298236*pi) q[0];
rz(1.357263603650812*pi) q[1];
rx(1.5707963267948966*pi) q[1];
rz(2.0779896335268964*pi) q[1];
rx(-1.5707963267948966*pi) q[1];
rz(-2.381184772407101*pi) q[1];
cz q[1], q[0];
rz(2.2478819429043635*pi) q[0];
rx(1.5707963267948966*pi) q[0];
rx(-1.5707963267948966*pi) q[1];
cz q[1], q[0];
rx(-1.5707963267948966*pi) q[0];
rx(1.5707963267948966*pi) q[1];
cz q[1], q[0];
rz(-1.5707963267948966*pi) q[7];
rx(1.5707963267948966*pi) q[7];
rz(1.5707963267948966*pi) q[7];
rx(-1.5707963267948966*pi) q[1];
cz q[2], q[1];
rx(1.5707963267948966*pi) q[1];
rz(-1.5707963267948966*pi) q[2];
rx(-1.5707963267948966*pi) q[2];
cz q[2], q[1];
rx(-1.5707963267948966*pi) q[1];
rx(1.5707963267948966*pi) q[2];
cz q[2], q[1];
rz(-1.5707963267948966*pi) q[4];
rx(1.5707963267948966*pi) q[4];
rz(1.5707963267948966*pi) q[4];
rz(-0.6542456812873576*pi) q[1];
rx(1.5707963267948966*pi) q[1];
rz(0.9242262418970197*pi) q[1];
rx(-1.5707963267948966*pi) q[1];
rz(-2.495242038915076*pi) q[1];
rz(2.17762946358662*pi) q[2];
rx(1.5707963267948966*pi) q[2];
rz(1.4086693904366439*pi) q[2];
rx(-1.5707963267948966*pi) q[2];
rz(-1.5707963267948966*pi) q[3];
rx(1.5707963267948966*pi) q[3];
rz(-2.557103588713229*pi) q[3];
rx(-1.5707963267948966*pi) q[3];
cz q[3], q[2];
rz(-1.6036095292257455*pi) q[2];
rx(-1.5707963267948966*pi) q[2];
rx(1.5707963267948966*pi) q[3];
cz q[3], q[2];
rz(-0.6542456812873576*pi) q[0];
rx(1.5707963267948966*pi) q[0];
rz(0.9242262418970197*pi) q[0];
rx(-1.5707963267948966*pi) q[0];
cz q[7], q[0];
rx(1.5707963267948966*pi) q[2];
cz q[2], q[1];
rx(-1.5707963267948966*pi) q[3];
cz q[4], q[3];
rz(-1.5707963267948966*pi) q[9];
rx(1.5707963267948966*pi) q[9];
cz q[9], q[8];
rz(1.5707963267948966*pi) q[12];
rx(1.5707963267948966*pi) q[12];
cz q[12], q[13];
rz(0.6463506146747173*pi) q[0];
rz(3.141592653589793*pi) q[1];
rz(2.5571035887132307*pi) q[2];
rx(-1.5707963267948966*pi) q[2];
rz(1.5707963267948966*pi) q[2];
rz(-2.2834146048500816*pi) q[3];
rz(-1.5707963267948966*pi) q[4];
rx(-1.5707963267948966*pi) q[4];
rz(1.5707963267948966*pi) q[4];
rz(-1.5707963267948966*pi) q[7];
rx(-1.5707963267948966*pi) q[7];
rz(1.5707963267948966*pi) q[7];
rz(3.141592653589793*pi) q[8];
rx(-1.5707963267948966*pi) q[9];
rz(1.5707963267948966*pi) q[9];
rx(-1.5707963267948966*pi) q[11];
rz(1.5707963267948966*pi) q[11];
rx(-1.5707963267948966*pi) q[12];
rz(1.5707963267948966*pi) q[12];
rz(3.141592653589793*pi) q[13];
rz(1.3280630244384688*pi) q[15];
rx(1.5707963267948966*pi) q[15];
rz(0.5753343373921794*pi) q[15];
rx(-1.5707963267948966*pi) q[15];
rz(2.5102265633964276*pi) q[15];