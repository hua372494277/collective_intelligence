#include <string>
#include <stdio.h>
#include <cmath>
#include <iostream>
#include <time.h>
using namespace std;

int squares[] = {0 , 1 , 4 , 9 , 16 , 25 , 36 , 49 , 64 , 81};
bool primes[1459];

bool isPrime(int n){
    if(n < 2){
        return false;
    }else{
        int sqr = (int)sqrt(n * 1.0);
        for(int i = 2 ; i <= sqr ; ++i){
            if(n % i == 0){
                return false;
            }
        }
        return true;
    }
}

struct item{
    char *nums;
    int sum;
    int square;
    struct item * next;
};

struct item * combinations[19];

void initIsPrime(){
    for(int i = 0 ; i < 1459 ; ++i){
        primes[i] = isPrime(i);
    }

	// initialize only one number in the chain
	combinations[1] = new struct item();
	combinations[1]->nums = new char();
	combinations[1]->nums[0] = 1;
	combinations[1]->sum = 1;
	combinations[1]->square = 1;
	struct item * pre = combinations[1];

	for(int i = 1; i < 10; i ++){
		struct item * p = new struct item();
		p->nums = new char();
		p->nums[0] = i;
		p->sum = i;
		p->square = squares[i];
		p->next = NULL;
		pre->next = p;
		pre = p;
	}
}

void addOneNum(int time){
	combinations[time] = new struct item();
	combinations[time]->nums = new char[time];
	combinations[time]->nums[0] = 1;

	struct item * lastChain = combinations[time-1];
	struct item * pre = combinations[time];// current chain to generate new items

	while(lastChain->next){
		lastChain = lastChain->next;

		//Time is from 1 - 18
		//But nums is starting from 0
		for(int i = 0; i <= lastChain->nums[time-2]; i ++){
			struct item * p = new struct item();

			p->nums = new char[time];
			// copy the high positions
			//such as, from the last chain, item 1,
			// generate 1*, then 1 should be copy to nums
			for(int j = 0; j < time - 1; j ++){
				p->nums[j] = lastChain->nums[j];
			}
			// generate the number on the lowest position
			// this number could not be larger than the number on higher positions
			p->nums[time - 1 ] = i;
			p->sum = i + lastChain->sum;
			p->square = squares[i] + lastChain->square;
			p->next = NULL;
			pre->next = p;
			pre = p;
		}
	}
}

void cleanPreChain(int time){
	struct item * cur = combinations[time];
	struct item * pre = cur;
	cur = cur->next;

	while(cur){
		if(primes[cur->sum] && primes[cur->square]){
			pre = cur;
			cur = cur->next;
			continue;
		}else{
			pre->next = cur->next;
			delete [] cur->nums;
			delete cur;
			cur = pre->next;
		}
	}
}

void combination(){
	struct item * pre = NULL;

	for(int time = 2; time < 19; time++){
		cout << time << "----------------------\n";
		addOneNum(time);
		cleanPreChain(time -1);
		pre = combinations[time];

		while( pre->next){
			pre = pre->next;
			for(int i  = 0; i < time; i++){
				printf("%d ", pre->nums[i]);
			}
			cout << "sum: " << pre->sum << " squ: " << pre->square << "\n";

		}

		if(time == 3){
			break;
		}
	}
}


int main()
{
	initIsPrime();
	combination();
	for(int time = 1; time < 3; time++){
		struct item * pre = combinations[time];
		while( pre->next){
			pre = pre->next;
			for(int i  = 0; i < time; i++){
				cout << (int)pre->nums[i] << " ";
			}
			cout << "sum: " << pre->sum << " squ: " << pre->square << "\n";

		}
	}



//	cout << lucky(1000, 100000);
//	long nume
//	unsigned long long x, y;
//
//	cout << max << "\n";
//	cout << max+1 << "\n";

//	for(int i = 0; i < 1460; i++){
//		cout << i << " -- " << get_is_prime(i) << "\n";
//	}

//	bitset3.reset();
//	bitset3.set(2);
//	bitset3.set(4);
//	bitset3.set(5);
//	t_start = time(NULL) ;
//	init_prime();
//	cout << lucky_number(1000, 100000000);
//	t_end = time(NULL) ;
//	printf("time: %f s\n", difftime(t_end,t_start)) ;
	return 1;
}

