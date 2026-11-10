    #include <iostream>
    using namespace std;

int gcd(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

int main() {
    int n1,n2,n3;
    int noc=0;
    cin>>n1>>n2>>n3;
    noc = n1*n2/gcd(n1,n2);
    noc = n3*noc/gcd(n3,noc);
    cout<<noc;
}