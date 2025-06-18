#include <stdio.h>
int proc( int A , int B ){
int c;
 int func(){
int d;
  L_0: d=4; //(:=,4,_,d)
 L_1: A=B; //(:=,B,_,A)
 L_2: c=d; //(:=,d,_,c)
 L_3: return c; //(rev,c,_,_)
}
 L_4: c=3; //(:=,3,_,c)
 L_5: printf("%d",A); //(out,A,_,_)
 L_6: printf("%d",B); //(out,B,_,_)
 L_7: func( ); //(call,func,_,_)
 L_8: printf("%d",A); //(out,A,_,_)
 L_9: printf("%d",B); //(out,B,_,_)
}
int main(){
int A;
 int B;
  L_10: A=1; //(:=,1,_,A)
 L_11: B=2; //(:=,2,_,B)
 L_12: if (A<B) goto L_14; //(<,A,B,19)
 L_13: goto L_15; //(jumb,_,_,20)
 L_14: A=1; //(:=,1,_,A)
 L_15: A=2; //(:=,2,_,A)
 L_16: proc(A,B); //(call,proc,_,_)
 L_17: printf("%d",A); //(out,A,_,_)
 L_18: printf("%d",B); //(out,B,_,_)
 L_19: {}
}