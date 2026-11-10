#include <iostream>
using namespace std;

int main(){
long int Fstart,Npr,Mot,DeMot;
cin >> Fstart >> Npr >> Mot >> DeMot;

 long int ratedtime[100];
long int realtime[100];
 
for (int i = 0; i < Npr; i++){
    cin >> ratedtime[i];
}
for (int i = 0; i < Npr; i++){
    cin >> realtime[i];
}
int count = 0;
for (int i = 0; i < Npr; i++){
    if (Fstart>0){
        if(realtime[i]< ratedtime[i]){
            Fstart += Mot;
        }
        else if (realtime[i] > ratedtime[i]){
            Fstart = Fstart - DeMot;
        }
        count++;

        Fstart = Fstart-realtime[i];
    }
}

 cout <<count;
}
