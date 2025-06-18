#include <stdio.h>
int main(){
int A;
 int B;
 int T;
 int T_0;
  L_0: A=0; //(:=,0,_,A)
 L_1: B=1; //(:=,1,_,B)
 L_2: T_0=A*B; //(*,A,B,T_0)
 L_3: T=T_0; //(:=,T_0,_,T)
 L_4: if (B>A) goto L_6; //(>,B,A,7)
 L_5: goto L_7; //(jumb,_,_,8)
 L_6: printf("%d",B); //(out,B,_,_)
 L_7: printf("%d",A); //(out,A,_,_)
 L_8: printf("%d",B); //(out,B,_,_)
 L_9: printf("%d",T); //(out,T,_,_)
 L_10: {}
}