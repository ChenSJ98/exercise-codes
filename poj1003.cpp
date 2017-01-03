#include<iostream>
#include<string>
using namespace std;
int judge(float l) {
	float i = 2;
	int n=0;
	float temp=0.00;
	while (temp <= l) {
		temp+= 1 / i;
		i++;
		n++;
	}
	return n;
}
int main() {
	float l=0.00;
	int a[200],i,n;
	n = 0;
	cin >> l;
	while (l != 0.00)
	{
		a[n]=judge(l);
		n++;
		cin >> l;
	}
	for (i = 0; i < n; i++)
		cout << a[i] << " card(s)"<<endl;
	return 0;
}
