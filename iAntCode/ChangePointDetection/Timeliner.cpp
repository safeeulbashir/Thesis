/*
 * Timeliner.cpp
 *
 *  Created on: Apr 16, 2015
 *      Author: safeeulbashir
 */
#include<fstream>
#include<iostream>
#include<string>
#include<vector>
using namespace std;

#define MINUTES 60
#define SEEDS_NUMBER 256;
vector <float> SUM;
/*#define MAX_ARRAY_SIZE MINUTES*60
 */
int MeanRateForRandomSeed = 0;
vector<int> OnePileTimeliner;
vector<int> FourPileTimeliner;
vector<int> SixteenPileTimeliner;
vector<int> SixtyFourPileTimeliner;
vector<int> RandomPileTimeliner;
vector<int> MasterTimeline;
vector<float> ChangePoints;
int searchForCollectedSeed(int PileType, int time, int slidingWindowSize) {
	int arrayRangeStart;
	int arrayRangeEnd;
	int startTime = time;
	int endTime = time + slidingWindowSize;
	int count = 0;
	if (PileType == 1) {
		arrayRangeStart = 1;
		arrayRangeEnd = 255;
	} else if (PileType == 4) {
		arrayRangeStart = 256;
		arrayRangeEnd = 511;
	} else if (PileType == 16) {
		arrayRangeStart = 512;
		arrayRangeEnd = 767;
	} else if (PileType == 64) {
		arrayRangeStart = 768;
		arrayRangeEnd = 1023;
	} else if (PileType == 0) {
		arrayRangeStart = 1024;
		arrayRangeEnd = 1279;
	} else if (PileType == -1) //For Random Distribution Only
			{
		arrayRangeStart = 0;
		arrayRangeEnd = 1279;
	}
	for (int i = arrayRangeStart; i <= arrayRangeEnd; i++) {
		if (startTime <= MasterTimeline[i] && MasterTimeline[i] <= endTime) {
			count++; //increase the number of seed count within a sliding window
		}
	}
	return count;

}
// For Random Seed Only
void MasterTimelinerCreator(char* fileName) {
	ifstream dataInput(fileName);
	string line;
	float pileID, DistributionType, XPosition, YPosition, CollectionTime, antID;
	if (dataInput.is_open()) {
		getline(dataInput, line);
		while (dataInput >> pileID >> DistributionType >> XPosition >> YPosition
				>> CollectionTime >> antID) {
			if (CollectionTime > 0) {
				CollectionTime = CollectionTime / 16;
				MasterTimeline.push_back((int) CollectionTime);
			} else
				MasterTimeline.push_back(-1);
		}
	}
	dataInput.close();

}
void MasterTimelinerCreator() {
	ifstream dataInput("iAntFoodPosition.txt");
	string line;
	float pileID, DistributionType, XPosition, YPosition, CollectionTime, antID;
	if (dataInput.is_open()) {
		getline(dataInput, line);
		while (dataInput >> pileID >> DistributionType >> XPosition >> YPosition
				>> CollectionTime >> antID) {
			if (CollectionTime > 0) {
				CollectionTime = CollectionTime / 16;
				MasterTimeline.push_back((int) CollectionTime);
			} else
				MasterTimeline.push_back(-1);
		}
	}
	dataInput.close();

}
void TimelineCreator(int pileType, int slidingWindowSize, int slidingAmount) {

	switch (pileType) {
	case 1:
		for (int i = 1; i < (MINUTES * 60 / slidingAmount);
				i = i + slidingAmount) {
			//implement Search
			int seed_count = searchForCollectedSeed(pileType, i,
					slidingWindowSize);

			OnePileTimeliner.push_back(seed_count);
		}
		break;
	case 4:
		for (int i = 1; i < (MINUTES * 60 / slidingAmount);
				i = i + slidingAmount) {
			//implement Search
			int seed_count = searchForCollectedSeed(pileType, i,
					slidingWindowSize);
			FourPileTimeliner.push_back(seed_count);
		}
		break;
	case 16:
		for (int i = 1; i < (MINUTES * 60 / slidingAmount);
				i = i + slidingAmount) {
			//implement Search
			int seed_count = searchForCollectedSeed(pileType, i,
					slidingWindowSize);
//					cout<<seed_count<<endl;
			SixteenPileTimeliner.push_back(seed_count);
		}
		break;
	case 64:
		for (int i = 1; i < (MINUTES * 60 / slidingAmount);
				i = i + slidingAmount) {
			//implement Search
			int seed_count = searchForCollectedSeed(pileType, i,
					slidingWindowSize);
			SixtyFourPileTimeliner.push_back(seed_count);
		}
		break;
	case 0:
		for (int i = 0; i < (MINUTES * 60 / slidingAmount);
				i = i + slidingAmount) {
			//implement Search
			int seed_count = searchForCollectedSeed(pileType, i,
					slidingWindowSize);
			RandomPileTimeliner.push_back(seed_count);
		}
		break;
	case -1:
		for (int i = 0; i < (MINUTES * 60 / slidingAmount);
				i = i + slidingAmount) {
			//implement Search
			int seed_count = searchForCollectedSeed(pileType, i,
					slidingWindowSize);
			RandomPileTimeliner.push_back(seed_count);
		}
		break;
	}
}

float meanCounter() {
	float mean;
	float sum = 0;
	for (int i = 0; i < RandomPileTimeliner.size(); i++) {
		sum = sum + RandomPileTimeliner[i];
		//cout<<sum<<endl;
	}
	//cout<<sum / RandomPileTimeliner.size()<<"From Mean";
	return (sum / RandomPileTimeliner.size());
}

void RandomSeedMeanFinder() {
	vector<float> a;
	vector<char*> FileNames;
	int sum=0;
	FileNames.push_back("iAntFoodPosition_RandomSeed_Experiment1_R800.txt");
	FileNames.push_back("iAntFoodPosition_RandomSeed_Experiment2_R100.txt");
	FileNames.push_back("iAntFoodPosition_RandomSeed_Experiment3_R200.txt");
	FileNames.push_back("iAntFoodPosition_RandomSeed_Experiment4_R400.txt");
	FileNames.push_back("iAntFoodPosition_RandomSeed_Experiment5_R1200.txt");
	for (int i = 0; i <FileNames.size(); i++) {
		MasterTimelinerCreator(FileNames[i]);
		TimelineCreator(-1, 60, 1);
		a.push_back(meanCounter());
		//cout<<a[i]<<endl;
		sum=sum+a[i];
		MasterTimeline.clear();
		RandomPileTimeliner.clear();
	}
	MeanRateForRandomSeed=sum/FileNames.size();
	cout<<MeanRateForRandomSeed;
}
float max (float a, float b) {
  return (a<b)?b:a;     // or: return comp(a,b)?b:a; for version (2)
}
void CUSUM()
{

	SUM.push_back(0.0);
	for(int i=1;i<OnePileTimeliner.size();i++)
	{
		//cout<<RandomPileTimeliner[i]<<endl;
		float temp=max(0,SUM[i-1]+OnePileTimeliner[i]-MeanRateForRandomSeed);
		if(temp>=MeanRateForRandomSeed)
			ChangePoints.push_back(i);
		SUM.push_back(temp);
	}
}


int main() {
	RandomSeedMeanFinder();//Getting the mean collection rate for Random Seeds
	 MasterTimelinerCreator(); //Creates Timelines for seeds time.
	 TimelineCreator(1, 60, 1); //Creates Timeline for OnePileType Seeds with 1 Seconds Sliding Window
	 TimelineCreator(4, 60, 1);
	 TimelineCreator(16, 60, 1);
	 TimelineCreator(64, 60, 1);
	 TimelineCreator(0, 60, 1);
	 cout << "Finished";

	 ofstream Timeliner("Timeliner.txt", ios::out);
	 for (int i = 0; i < OnePileTimeliner.size(); i++)
	 Timeliner << OnePileTimeliner[i] << "\t" << FourPileTimeliner[i] << "\t"
	 << SixteenPileTimeliner[i] << "\t" << SixtyFourPileTimeliner[i]
	 << "\t" << RandomPileTimeliner[i] << "\t" << endl;
//	 Timeliner<<OnePileTimeliner[i]<<endl;
	 CUSUM();
	 ofstream CUSUM("CUSUM.txt");
	 for(int i=0;i<ChangePoints.size();i++)
		 CUSUM<<ChangePoints[i]<<endl;
	 ofstream SUMM("SUM.txt");
		 for(int i=0;i<SUM.size();i++)
			 SUMM<<SUM[i]<<endl;


}

