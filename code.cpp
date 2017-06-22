#include <string>
#include <stdio.h>
#include <cmath>
#include <iostream>
#include <time.h>
#include <bitset>
#include <fstream>
using namespace std;

int squares[] = {0 , 1 , 4 , 9 , 16 , 25 , 36 , 49 , 64 , 81};
bool primes[1459];

ofstream myfile;

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

struct num_List{
    unsigned long long num;
    struct num_List * next;
};

struct num_List * num_list_head;
struct num_List * num_list_cur;

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

    num_list_head = new struct num_List();
    num_list_head->num = 0;
    num_list_head->next = NULL;
    num_list_cur = num_list_head;
}

int is_swap(char *str, int begin, int k){
    int i, flag;

    for (i = begin, flag = 1; i < k; i ++) {
        if (str[i] == str[k]) {
            flag = 0;
            break;
        }
    }

    return flag;
}

void swap(char *str, int a, int b)
{
    char temp;
    temp = str[a];
    str[a] = str[b];
    str[b] = temp;
}

void permutation_process(char *nums, int begin, int end, unsigned long long base) {
    int k;

    if (begin == end - 1)
    {
        unsigned long long index = 0;
        myfile << "Output: ";
        for (int i = 0; i < end; i++){
        	myfile << (int) nums[i] << ", ";
        	cout << (int) nums[i] << ", ";
        }
        myfile << base << "\n";
        cout << base << "\n";
        for(int i = end - 1; i > -1; i --){
            index += base * ((int) nums[i]);
            base *= 10;
        }
        num_list_head->num += 1;
        struct num_List * p = new struct num_List();
        p->num = index;
        p->next = NULL;
        num_list_cur->next = p;
        num_list_cur = p;
    }
    else
    {
        for (k = begin; k < end; k ++)
        {
            if (is_swap(nums, begin, k))
            {
                swap(nums, k, begin);
                permutation_process(nums, begin + 1, end, base);
                swap(nums, k, begin);
            }
        }
    }
}

void addAndDeleteOneNum(int time){
	// initialize the head node
	// the nums[0] saved how many digits in each numbers
    combinations[time] = new struct item();
    combinations[time]->nums = new char[time];
    combinations[time]->nums[0] = time;
    struct item * pre = combinations[time];// current chain to generate new items

    struct item * preLastChain = combinations[time-1];
    struct item * curLastChain = preLastChain->next;

    while(curLastChain){
        //Time is from 1 - 18
        //But nums is starting from 0
        for(int i = 0; i <= curLastChain->nums[time-2]; i ++){
            if(time == 18 && (!primes[i + curLastChain->sum]|| !primes[squares[i] + curLastChain->square])){
                continue;
            }
            struct item * p = new struct item();
            p->nums = new char[time];
            // copy the high positions
            //such as, from the last chain, item 1,
            // generate 1*, then 1 should be copy to nums
            for(int j = 0; j < time - 1; j ++){
                p->nums[j] = curLastChain->nums[j];
                myfile << (int) p->nums[j] << ", ";
                cout << int(p->nums[j])<< ",";
            }
            // generate the number on the lowest position
            // this number could not be larger than the number on higher positions
            p->nums[time - 1 ] = i;
            myfile << (int) p->nums[time - 1] << "\n";
            cout <<  (int)p->nums[time - 1] << "\n";
            p->sum = i + curLastChain->sum;
            p->square = squares[i] + curLastChain->square;
            p->next = NULL;
            pre->next = p;
            pre = p;
        }

        // Deal with the nodes on last chain
        // If it is not prime number
        // Delete this node from last chain
        if(primes[curLastChain->sum] && primes[curLastChain->square]){
        	unsigned long long base = 1;
			int len = time - 1;

			for (int i = time - 2; i >= 0 && curLastChain->nums[i] == 0; i--) {
				base *= 10;
				len --;
			}
			permutation_process(curLastChain->nums, 0, len, base);
		}
		preLastChain->next = curLastChain->next;
		delete [] curLastChain->nums;
		delete curLastChain;
		curLastChain = preLastChain->next;
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



void setBitBaseNums(char * nums, int time){
    unsigned long long base = 1;
    int len = time;

    for (int i = time - 1; i >= 0 && nums[i] == 0; i--) {
        base *= 10;
        len --;
    }
    permutation_process(nums, 0, len, base);
}

void setBitForNum(int time){
    struct item * cur = combinations[time];
    struct item * pre = cur;
    cur = cur->next;

    while(cur){
        setBitBaseNums(cur->nums, time);
        pre->next = cur->next;
        delete [] cur->nums;
        delete cur;
        cur = pre->next;
    }

    delete [] combinations[time]->nums;
    delete combinations[time];
}

void combination(){
    for(int time = 2; time < 19; time++){
    	addAndDeleteOneNum(time);
        //cleanPreChain(time - 1);
        //setBitForNum(time - 1);
    }
//    cleanPreChain(18);
    setBitForNum(18);
}


int main()
{
	myfile.open("C:\\computer_science_y\\version_control\\collective_intelligence\\example.csv");
//	myfile << "Writing this to a file.\n";

    unsigned long long x = 1, y = 100000000;
    //cin >> x >> y;
    unsigned long long count = 0;
    initIsPrime();
    combination();

    struct num_List * p = num_list_head;
    p = p->next;

    while (p) {
        if(p->num < y && p->num > x){
            count ++;
        }
        p = p->next;
    }
    cout << count;
    myfile.close();
//    num_list.set(n);
    //    unsigned long count = 0;
//    for(int time = 2; time < 19; time++){
//        struct item * pre = combinations[time];
//        while( pre->next){
//            pre = pre->next;
//            count ++;
//        }
//    }
//    cout << count;


    //	bitset3.reset();
    //	bitset3.set(2);
    //	bitset3.set(4);
    //	bitset3.set(5);
    //	t_start = time(NULL) ;
    //	init_prime();
    //	cout << lucky_number(1000, 100000000);
    //	t_end = time(NULL) ;
    //	printf("time: %f s\n", difftime(t_end,t_start)) ;
}
