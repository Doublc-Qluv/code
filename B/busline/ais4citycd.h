#ifndef __AIS4CITYCD_H
#define __AIS4CITYCD_H
#include"basic_types.h"
#include <stdio.h>
#define BACKSEARCH		//反向搜索
#define MINIBREAKV 2		//在该换乘次数以上采用反向搜索
#define SAME2SAME			//路线中有重复的站的情况
//用于描述方案DAG图
#define	ENDFLAG	0xffff
#define	BLFLAG		0xfffe
//#define CHECKARRAY
typedef struct bus
{
	UINT16	type;
	UINT16	station_count;
	char*	name;				//point to MainData.pString
	char*	description;			//point to MainData.pString
	UINT16*	pStation_array;		//point to MainData.pStation_array
}Bus;
typedef struct station
{
	UINT16	number;
	UINT16	bus_count;
	char*	name;				//point to MainData.pString
//	char*	description;			//point to MainData.pString
	UINT16*	pBus_array;			//point to mainData.pBus_array
}Station;

typedef struct {
	UINT16	solutionData_len;
	UINT16	station_S;
	UINT16	station_D;
	UINT16	stationCnt;
	UINT16	busCnt;
	UINT16	transfer_times;
	UINT16	miniCost;
	UINT16	station_S_offset;
	UINT16	body_len;
	UINT16	string_len;
//	UINT16*	pSolutionData;	//(UINT16*)pSoultionHead+10+4*3;
	UINT8*	pString;			//pStringIndex+string_len;
}SoultionHead;

#define MAX_CITYNAME_LEN	62
#define MAXTRANS_TIMES		8
typedef struct mainData
{
//Bus and Station
	UINT16			bus_count;
	UINT16			na_bus_count;
	UINT16			station_count;	/*  OK*/
	UINT8			city_name[MAX_CITYNAME_LEN];			
	Bus*			pBus;			//pbus = MALLOC(sizeof(Bus)*bus_count);
	UINT16*			pBus_array;
	UINT32			Len_pBus_array;
	Station*			pStation;		//pstation = MALLOC(sizeof(Station)*station_count);
	UINT16*			pStation_array;
	UINT32			Len_pStation_array;
//transfer times matrix
	UINT8*			ptransfer_times; //if 2bits,the size of it is (station_count^2*2+7)/8, if station_count of CD is about 1500, then the size of  transfer_times is 540KB.
//use to stroge all string data
	char*			pString;			//pString = MALLOC(sizeof(char)*Len_pString);
	UINT32			Len_pString;		/*  OK*/
#ifdef FAST_H_SEARCH
	UINT8*			hData_Bus2Bus;
	UINT8*			hData_Sta2Sta;
	UINT8			hData_bpp;
#endif
}MainData;
#define MAX_TRANSF_TIMES 10
typedef struct busSearchEngine
{
	MainData* pData;
	UINT8	*mem_pool;
	UINT16	*miniCost_S;
	UINT16	*miniCost_D;
	UINT16	*StaDataLen;
	UINT16	*solutionData;
	UINT16	*pBusQ;
	UINT8	*miniTranTimes;
	UINT8	*fg_BL;
	UINT8	*fg_ST;
	UINT8	*fg_STE;
	UINT8	*fg_CirLine;
	UINT16	DataSize;
	UINT16	exCnt;
	UINT16	solutionDataLen;
	UINT16	DataSize3;
	UINT16* pBusNo, *pBusNo2,*pStaNo;/*脫脙脫脷麓忙路脜脙驴赂枚脮戮碌脛脡脧鲁碌鲁碌潞脜拢卢卤脺脙芒禄禄脥卢脪禄麓脦鲁碌*/
	UINT8 *pStaBeExiest;
	
	UINT16* pQueue ,*pBusBeS, *pTempQueue;
	UINT16 que_top,que_bot, Is_top_bot;
	UINT  expandedNodeCnt, LastCmp;
	UINT16	Lay_cost_Len[MAX_TRANSF_TIMES], Sline[MAX_TRANSF_TIMES*3];
	UINT8 ret, firstIn, tranferTimes;
	UINT16 Station_D;
	UINT16 DataLen2;
	UINT16 *pStaInQueue;
	
	UINT16 exDistance;

	UINT16 MaxDirOffset;
	UINT16* tempArray;

	char* output;
	int	outputLen;
	int	loadFromFile;
	char tempString[1024];
	UINT16	(*SearchDAG_depth)(
		struct busSearchEngine* const pBusSearchEngine,
		UINT16 StaS,
		UINT16 cost,	
		UINT16 preBusNo,
		UINT8 depth,
		const UINT8 MaxDepth,
		const UINT16 miniCost);
	void (*SearchDAG_depth4Bulid)(
		struct busSearchEngine* const pBusSearchEngine,
		UINT16 StaS,
		UINT16 cost,
		UINT16 preBusNo,
		UINT8 depth,
		const UINT8 MaxDepth,
		const UINT16 miniCost);
	UINT (*CompleteSolutionStream)(struct busSearchEngine* const pBusSearchEngine, UINT16* pSolutionData);
	UINT (*ReviewSolutionStream)(struct busSearchEngine* const pBusSearchEngine,UINT16* pSolutionData);
	UINT (*BuildSolutionStream)(
		struct busSearchEngine* const pBusSearchEngine,
		UINT16 StaS,
		UINT16 cost,
		UINT16 preBusNo,
		UINT8 depth,
		const UINT8 MaxDepth,
		const UINT16 miniCost,
		const UINT16 StaD);
	UINT (*SearchLine_WR)(struct busSearchEngine* const pBusSearchEngine, const UINT16 station_S, const UINT16 station_D);
	UINT (*SlineToString)(struct busSearchEngine* const pBusSearchEngine, const UINT16* Sline);
	void (*DBusSearchEngine)(struct busSearchEngine** ppBusSearchEngine);
}BusSearchEngine;
#endif
