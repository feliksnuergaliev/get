#include <iostream>
using std::cout;
using std::endl;
using std::cin;
unsigned int sum_ternary(unsigned int a);
unsigned int sum_ternary(unsigned int a)
{
    int c=0;
    while(a>0){
        c += a%3;
        a/=3;

    }
    return c;
}
// ваша реализация функции
int main()
{
    unsigned int n, s = 0, tmp;
    cin >> n;
    for (unsigned int i = 0; i < n; i++)
    {
        cin >> tmp;
        s += sum_ternary(tmp);
    }
    cout << sum_ternary(s) << endl;
    return 0;
}