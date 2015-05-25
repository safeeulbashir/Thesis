#include<iostream>
#include<fstream>
#include<string>
#include<vector>
#include "iAnt_food_type.h"
using namespace std;
#define MAX_MIN 412
int main() {
	ofstream CumRate("CumRatePerMin.txt", ios::out);
	vector<iAnt_food_type> InitialFoodPositions;
	string line;
	int OnePileType[MAX_MIN] = { 0 };
	int FourPileType[MAX_MIN] = { 0 };
	int SixteenPileType[MAX_MIN] = { 0 };
	int SixtyfourPileType[MAX_MIN] = { 0 };
	int UniformSeeds[MAX_MIN] = { 0 };
	cout << "Hello World\n";
	ifstream myfile("iAntFoodPosition.txt");
	iAnt_food_type tempLocation;
	float maxTime = 0;
	float pileID, DistributionType, XPosition, YPosition, CollectionTime;
	if (myfile.is_open()) {
		getline(myfile, line);
		while (myfile >> pileID >> DistributionType >> XPosition >> YPosition
				>> CollectionTime) {
			tempLocation.setPileId(pileID);
			tempLocation.setDistributionType(DistributionType);
			tempLocation.setXPosition(XPosition);
			tempLocation.setYPosition(YPosition);
			tempLocation.setCollectionTime(CollectionTime / (16 * 60));
			InitialFoodPositions.push_back(tempLocation);
			if (maxTime < CollectionTime / (16 * 60))
				maxTime = CollectionTime / (16 * 60);
			//cout<<tempLocation.getCollectionTime()<<endl;
		}
		//cout<<maxTime;
		//cout<<InitialFoodPositions.size();
		myfile.close();
		for (int i = 0; i < InitialFoodPositions.size(); i++) {
			if (i <= 255) {
				OnePileType[int(InitialFoodPositions[i].getCollectionTime())]++;
			} else if (i <= 511) {
				FourPileType[int(InitialFoodPositions[i].getCollectionTime())]++;
			} else if (i <= 767) {
				SixteenPileType[int(InitialFoodPositions[i].getCollectionTime())]++;
			} else if (i <= 1023) {
				SixtyfourPileType[int(
						InitialFoodPositions[i].getCollectionTime())]++;
			} else {
				UniformSeeds[int(InitialFoodPositions[i].getCollectionTime())]++;
			}
		}
		for(int i=1;i<MAX_MIN;i++)
		{
			OnePileType[i]=OnePileType[i-1]+OnePileType[i];
			FourPileType[i]=FourPileType[i-1]+FourPileType[i];
			SixteenPileType[i]=SixteenPileType[i-1]+SixteenPileType[i];
			SixtyfourPileType[i]=SixtyfourPileType[i-1]+SixtyfourPileType[i];
			UniformSeeds[i]=UniformSeeds[i-1]+UniformSeeds[i];
		}
		CumRate<<"Minute\tOne Pile\tFour Pile\tSixteen Pile\tSixty Four Pile\t Uniform Seeds"<<endl;
		for(int i=0;i<MAX_MIN;i++){
			//cout<<i;
			CumRate<<i<<"\t"<<OnePileType[i]<<"\t"<<FourPileType[i]<<"\t"<<SixteenPileType[i]<<"\t"<<SixtyfourPileType[i]<<"\t"<<UniformSeeds[i]<<endl;
			cout<<i<<"\t"<<OnePileType[i]<<"\t"<<FourPileType[i]<<"\t"<<SixteenPileType[i]<<"\t"<<SixtyfourPileType[i]<<"\t"<<UniformSeeds[i]<<endl;
		}
			CumRate.close();
	}

	else
		cout << "Unable to open file";
	return 0;
}

