/*
 * iAnt_food_type.h
 *
 *  Created on: Apr 2, 2015
 *      Author: safeeulbashir
 */

#ifndef IANT_FOOD_TYPE_H_
#define IANT_FOOD_TYPE_H_
class iAnt_food_type{
public:
	float getCollectionTime() const {
		return collectionTime;
	}

	void setCollectionTime(float collectionTime) {
		this->collectionTime = collectionTime;
	}

	int getDistributionType() const {
		return DistributionType;
	}

	void setDistributionType(int distributionType) {
		DistributionType = distributionType;
	}

	int getPileId() const {
		return PileId;
	}

	void setPileId(int pileId) {
		PileId = pileId;
	}

	float getXPosition() const {
		return XPosition;
	}

	void setXPosition(float position) {
		XPosition = position;
	}

	float getYPosition() const {
		return YPosition;
	}

	void setYPosition(float position) {
		YPosition = position;
	}

private:
	int PileId;
	int DistributionType;
	float collectionTime;
	float XPosition;
	float YPosition;
};



#endif /* IANT_FOOD_TYPE_H_ */
