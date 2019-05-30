#ifndef __BUS_ENGINE_H
#define __BUS_ENGINE_H
#include "basic_types.h"
UINT MyReadFile(char* fname, UINT32 *Len);
UINT CBusSearchEngine(UINT8* stream);
UINT Engine_LoadData(char fileName[]);
UINT Engine_SearchLine(UINT engineHandle, UINT16 Sta_S, UINT16 Sta_D);
UINT Engine_SearchLine_org(UINT engineHandle, UINT16 Sta_S, UINT16 Sta_D);
UINT Engine_Destroy(UINT engineHandle);
UINT Engine_GetStationCount(UINT engineHandle);
UINT Engine_GetBuslineCount(UINT engineHandle);
UINT Engine_GetBuslineDesc(UINT engineHandle, UINT16 buslineIndex);
UINT Engine_GetStationName(UINT engineHandle, UINT16 stationIndex);
UINT Engine_GetBuslineName(UINT engineHandle, UINT16 buslineIndex);
UINT Engine_SetExDistance(UINT engineHandle, UINT16 exDistance);
UINT Engine_GetExDistance(UINT engineHandle);
UINT Engine_GetCityName(UINT engineHandle);
UINT Engine_GetStaCntInBusline(UINT engineHandle, UINT16 buslineIndex);
UINT Engine_GetBusCntInStation(UINT engineHandle, UINT16 stationIndex);
UINT Engine_GetStaInBusline(UINT engineHandle, UINT16 buslineIndex, UINT16 staInbusNo);
UINT Engine_GetBusInStation(UINT engineHandle, UINT16 stationIndex, UINT16 busInstaNo);
#endif
