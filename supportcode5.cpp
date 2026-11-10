#include <iostream>
#include <unistd.h> // Required for sysconf(_SC_AVPHYS_PAGES)
#include <typeinfo> // Required for typeid

using std::cout, std::endl;

void Inc(int *px); //Функция для работы с указателем
       
int main()
{   
    {
        int x = 2;                         //Обычная переменная
        int *px = &x;                      //Указатель на нее
   
        cout << "x     is \t" << x << endl;      //Наша переменная
        cout << "px=&x is \t" << px << endl;     //Указатель - это номер ячейки памяти, где хранится значение x
        cout << "*px   is \t" << *px << endl;    //Доступ к значению по адресу
        cout << "typeid(x) is \t" << typeid(x).name() << endl;  //Как компилятор видит типы x и px
        cout << "typeid(px) is \t" << typeid(px).name() << endl;

    }
    
    //Разберемся с синтаксисом *
    {
        int x = 2;
        int *p1  = &x; //
        int* p2  = &x; // Это все одно и то же. А почему?
    }
    
    //int x = 2;                         
    //int *px = &x;                      
    //px = x; //Как на px смотрит компилятор?
    ///error: invalid conversion from ‘int’ to ‘int*’
    //То есть тип переменной px - это int* 

    //Но есть проблема:
    {
        int* p1, p2;
        cout << "\nint* p1, p2;\n";
        cout << "typeid(p1) is \t" << typeid(p1).name() << endl;
        cout << "typeid(p2) is \t" << typeid(p2).name() << endl;
        //То есть int* не работает так, как мы этого ожидаем   
    }

    //От нас ожидают чего-то такого:
    {
        int *p1, *p2;
        cout << "\nint *p1, *p2;\n";
        cout << "typeid(p1) is \t" << typeid(p1).name() << endl;
        cout << "typeid(p2) is \t" << typeid(p2).name() << endl; 
    }

    //Это можно обойти через псевдоним типа:
    {
        using intptr = int*; //Конечно, заниматься таким на полном серьезе не нужно
        intptr p1, p2;       //Но это дает нам понять, как со времнем развивалась концепция c++
        cout << "\nusing iptr = int*;\niptr p1, p2;\n";
        cout << "typeid(p1) is \t" << typeid(p2).name() << endl;
        cout << "typeid(p2) is \t" << typeid(p2).name() << endl;
    }    

    //Для нас главное, понять как именно все работает. И правильно пользоваться тем, что дали:
    int x = 2, *px = &x;
    cout << "\nint x = 2, *px = &x;\n";
    cout << "*px   is \t" << *px << endl;    
    
    //Функции и указатели
    cout<<"\nInside the MAIN\n";
    cout<<"&px is   \t"<<&px<<endl;    //Указатель на указатель (адрес переменной, которая хранит адрес)
    Inc(px);                           //Передаем указатель в функцию. Можно просто Inc(&x);
    cout<<"Back to the MAIN\n";
    cout <<"x is    \t"<< x<<" now\n"; //Значение переменной успешно изменилось
    cout<<"px=&x is \t"<<px<<endl;     //Указатель не испортился
    
    //Двойные указатели - это указатели на указатели
    //int **ppx = &&x;                 //Так нельзя
    int **ppx = &px;                   //А так можно
    

    //Массивы - это указатели
    cout<<"\nArrayz\n\n";
    cout<<"int* M1\n";
    int n = 10;
    //cin>>n; //Наконец так стало можно.
    int* M1 = new int[n]; //Память взяли
    for(int i=0; i<n; i++)
        M1[i] = i; // *(M1+i) = i; - теперь мы понимам, как это работает
    int* N1 = M1; //Мы копируем не весь массив, а только указатель на его начало.
    N1[n/2] = 100500;   
    for(int i=0; i<n; i++) 
        cout << M1[i] << ' ';
    
    delete[] M1;           //Память вернули
    //delete[] N1;         //А это ошибка. Память брали только один раз.
    ///Invalid free() / delete / delete[] / realloc()
    ///at 0x484CA8F: operator delete[](void*) (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
    ///by 0x109A3D: main (...)
    ///Address 0x4dee0c0 is 0 bytes inside a block of size 40 free'd
    
    cout<<"\n\nint** M2\n";
    int** M2 = new int*[n]; //Двухмерные массивы это на самом деле одномерные массивы указателей
    for (int i=0; i<n; i++)
    {
        M2[i] = new int[i+1];
        for(int j=0;j<i+1;j++) //Хочу треугольный двухмерный массив
        {
            M2[i][j]=j;
            cout<<M2[i][j]<<' ';
        }
        cout<<endl;
    }
    //Очищаем память
    for(int i=0;i<n;i++) //Освобождаем сами данные
        delete[] M2[i];
    delete[] M2; //Освобождаем массив ссылок на строки

    cout<<"\n\nint**** M4\n";
    int**** M4 = new int ***[n]; //Четырехмерный массив? Да легко!
    for (int i=0; i<n; i++)
    {
        M4[i]= new int**[n];
        for (int j=0;j<n;j++)
        {
            M4[i][j]=new int*[n];
            for (int k=0;k<n;k++)
            {
                M4[i][j][k]=new int[n];
                for (int l=0;l<n;l++)
                {
                    M4[i][j][k][l]=i+j+k+l;
                }
            }
        }
    }

    M4[0][0][0][0]=1234;
    cout<<"M4[0][0][0][0] is " << ****M4 <<endl;
    cout<<"M4[1][2][3][4] is " <<M4[1][2][3][4]<<" or "<< *(*(*(*(M4+1)+2)+3)+4)<<endl;
    for (int i=0; i<n; i++) //Очищаем все это великолепие
    {
        for (int j=0;j<n;j++)
        {
            for (int k=0;k<n;k++)
                delete[] M4[i][j][k];//Порядок важен! Если сперва освободим верний уровень ссылок,
            delete[] M4[i][j];       //не сможем добраться до нижнего
        }
        delete[] M4[i];
    }
    delete[] M4;

    //Почему за памятью нужно следить?
/*
    cout<<"\nMemory leakage\n\n";//утечка памяти
    long long mem = sysconf(_SC_AVPHYS_PAGES); //Сколько у нас есть памяти?
    cout<<"My memmory was       "<<sysconf(_SC_AVPHYS_PAGES)<<endl;
    while (sysconf(_SC_AVPHYS_PAGES)>mem/8)
        {
            int* arr = new int[1000000];
            arr[0]=1; arr[1000000-1]=arr[0];//Делаем что-то нужное и важное
            //delete[] arr //Ой, забыли
        }
    cout<<"but now it\'s only   " << sysconf(_SC_AVPHYS_PAGES)<<endl;
*/    
    return 0;
}

void Inc(int *px)
{
    cout<<"Inside the function\n";
    cout<<"x=*px is  \t"<<*px<<endl; //Значение переменной по полученному адресу
    cout<<"px is     \t"<<px<<endl;  //Сам адрес
    cout<<"&px is    \t"<<&px<<endl; //Адрес адреса (А это уже копия)
    (*px)++;
    //*px++; //Оператор * имеет возмутительно низкий приоритет!
    px = 0; //Можно испортить сам указатель, это всего лишь копия
    cout<<"mod px is \t"<<px<<endl;
}
