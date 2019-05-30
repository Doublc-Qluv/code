#include "ais4citycd.h"

//#define DEBUG

#ifdef DEBUG
#define DEBUG_PRINTF printf
#else
#define DEBUG_PRINTF(...)
#endif

#define NEWLINE 			'\n'
#define END				'\0'
#define FILE_END_CHAR	'#'
#define DESCRIPT_CHAR	':'
#define NEXT_STATION	'-'
#define BACK_CHAR		'b'
#define FORCE_CHAR		'f'
#define LOOP_CHAR		'r'
#define BUSLINE_NAME		0
#define BUSLINE_CONTENT	1
#define BUSLINE_DESCRIPT	2

#define MYFREE(a) {if(a != NULL) FREE(a);a=NULL;}

UINT MyReadFile(char* fname, UINT32 *Len)
{
	FILE*	pf = NULL;
	UINT8*	stream=NULL;
	UINT32	fileLen;
	pf = fopen( fname, "rb");
	if(pf == NULL)
	{
		DEBUG_PRINTF("Open file:%s failure!\n", fname);
		return (UINT)NULL;
	}
	DEBUG_PRINTF("Open file:%s success!\n", fname);
	fseek(pf, 0, SEEK_END);
	fileLen = ftell(pf);
	fseek(pf, 0, SEEK_SET);
	if((stream = (UINT8*)MALLOC(fileLen)) == NULL)
		return (UINT)NULL;
	
	fread(stream, fileLen, 1 , pf);
	*Len = fileLen;
	fclose(pf);
	return (UINT)stream;
}

static MainData* loadData(UINT8* stream)
{
	UINT32	offset=0, i;
	INT32	pnOffset_pBus_array=0, pnOffset_pStation_array=0, pnOffset_pString=0;
	
	UINT32	num;
	MainData	baseData;
	MainData* pMain_data = NULL;
	if(stream == NULL)
		return NULL;
	MEMCPY(&baseData, stream, sizeof(MainData));
	
	pMain_data = (MainData*)stream;
	offset+=sizeof(MainData);
	
	pMain_data->pBus				= (Bus*)(stream + offset);
	offset+=pMain_data->bus_count * sizeof(Bus);
	
	pMain_data->pStation			= (Station*)(stream + offset);
	offset+=pMain_data->station_count * sizeof(Station);
	
	pMain_data->pBus_array		= (UINT16*)(stream + offset);
	offset+=pMain_data->Len_pBus_array * sizeof(UINT16);
	
	pMain_data->pStation_array	= (UINT16*)(stream + offset);
	offset+=pMain_data->Len_pStation_array * sizeof(UINT16);
	
	pMain_data->pString			= (char*)(stream + offset);
	offset+=pMain_data->Len_pString * sizeof(UINT8);

	pnOffset_pBus_array		= (INT32)((UINT32)baseData.pBus_array - (UINT32)pMain_data->pBus_array);
	pnOffset_pStation_array	= (INT32)((UINT32)baseData.pStation_array - (UINT32)pMain_data->pStation_array);
	pnOffset_pString		= (INT32)((UINT32)baseData.pString - (UINT32)pMain_data->pString);
	for(i = 0; i<pMain_data->bus_count; i++)
	{
		num = (UINT32)(pMain_data->pBus[i].name);
		num -= pnOffset_pString;
		pMain_data->pBus[i].name = (char*)num;

		num = (UINT32)(pMain_data->pBus[i].description);
		num -= pnOffset_pString;
		pMain_data->pBus[i].description = (char*)num;

		num = (UINT32)(pMain_data->pBus[i].pStation_array);
		num -= pnOffset_pStation_array;
		pMain_data->pBus[i].pStation_array = (UINT16*)num;
	}
	for(i = 0; i<pMain_data->station_count; i++)
	{
		num = (INT32)pMain_data->pStation[i].name;
		num -= pnOffset_pString;
		pMain_data->pStation[i].name = (char*)num;

		num = (INT32)pMain_data->pStation[i].pBus_array;
		num -= pnOffset_pBus_array;
		pMain_data->pStation[i].pBus_array = (UINT16*)num;
	}
	
	return pMain_data;
}

#define USEMASK 0


#define GetFlag(pFlag, i)	(pFlag[i>>3] & (1 <<(7-i&7)))
#define SetFlagTrue(pFlag, i)	(pFlag[i>>3] = pFlag[i>>3]|(1 <<(7-i&7)))
#define SetFlagFalse(pFlag, i)	(pFlag[i>>3] = pFlag[i>>3]&~(1 <<(7-i&7)))


static UINT16 SearchDAG_depth(
	struct busSearchEngine* const pBusSearchEngine,
	UINT16 StaS, 				//µ±Ç°Õ¾
	UINT16 cost, 					//µ±Ç°Õ¾µÄ´ú¼Û
	UINT16 preBusNo,
	UINT8 depth,
	const UINT8 MaxDepth,
	const UINT16 miniCost
	)
{
	int i,j,k,lastSpos;
	UINT16 busCnt=pBusSearchEngine->pData->pStation[StaS].bus_count;
	UINT16* pBus_array=pBusSearchEngine->pData->pStation[StaS].pBus_array;
	UINT16 busNo, staCnt, currentSta, curCost;
	UINT16 outDegreeCnt=0, acBusCnt=0;
	UINT flag;
	pBusSearchEngine->exCnt++;
	for(i=0; i<busCnt; i++)
	{
		busNo=pBus_array[i];
		if(preBusNo == busNo)//Ò»¶¨ÒªÓÐ£¬²»È»¿ÉÄÜ»áÖ´ÐÐacBusCnt++;
			continue;
		flag=0;
		k=0;while(pBusSearchEngine->pData->pBus[busNo].pStation_array[k]!=StaS) k++;
		staCnt=pBusSearchEngine->pData->pBus[busNo].station_count;
		curCost=cost;
		if(pBusSearchEngine->pData->pBus[busNo].type != 0)
		{
			lastSpos = k;
			for(j=k+1; j<staCnt; j++)
			{
				if(curCost++>(miniCost-2 + pBusSearchEngine->exDistance))
#ifdef SAME2SAME
				{
					while(j<staCnt)
					{ 
						if(pBusSearchEngine->pData->pBus[busNo].pStation_array[j]==StaS)
							break;
						j++;
					}
					if(j >= staCnt)
						break;
					else
					{
						curCost = cost;
						continue;
					}
				}
#else
					break;
#endif
				
				currentSta = pBusSearchEngine->pData->pBus[busNo].pStation_array[j];
#ifdef SAME2SAME
				if(currentSta == StaS)
				{
					curCost = cost;
					lastSpos = j;
					continue;
				}
#endif
				if(curCost != pBusSearchEngine->miniCost_S[currentSta] || pBusSearchEngine->miniTranTimes[currentSta] != depth+1 || pBusSearchEngine->miniCost_S[StaS]==0xfdfd)
					continue;
				if(pBusSearchEngine->miniCost_D[currentSta])
				{
				//Èç¹ûµ±Ç°Õ¾µÄºó¼ÌÕ¾currentStaÔÚ×î¼ÑÂ·¾¶ÉÏ
					
					if(pBusSearchEngine->miniCost_D[currentSta]+curCost <= miniCost + pBusSearchEngine->exDistance)
					{
					//µ±Ç°Õ¾StaSÔÚ×î¼ÑÂ·¾¶ÉÏ
						SetFlagTrue(pBusSearchEngine->fg_ST,currentSta);
						SetFlagTrue(pBusSearchEngine->fg_ST,StaS);
						
						if(MaxDepth == depth+1)//currentStaÄÜÖ±´ïÄ¿µÄÕ¾£¬ÇÒÔÚ×î¼ÑÂ·¾¶ÉÏ
							pBusSearchEngine->StaDataLen[currentSta] = 0xffff;
						if(!pBusSearchEngine->miniCost_D[StaS])
						{
							pBusSearchEngine->miniCost_D[StaS] = 
								curCost + pBusSearchEngine->miniCost_D[currentSta] - pBusSearchEngine->miniCost_S[StaS];
						}else
							if(pBusSearchEngine->miniCost_D[StaS] > curCost - pBusSearchEngine->miniCost_S[StaS] + pBusSearchEngine->miniCost_D[currentSta])
								pBusSearchEngine->miniCost_D[StaS]=curCost - pBusSearchEngine->miniCost_S[StaS] + pBusSearchEngine->miniCost_D[currentSta];
						//ÕÒµ½Ò»ÌõÂ·¾¶
		//				DEBUG_PRINTF("%d: %s\n",currentSta, pData->pStation[currentSta].name);
		//				DEBUG_PRINTF("%s\n", pData->pBus[busNo].name);
						outDegreeCnt++;
						flag = 1;
					}
				}
				else if(MaxDepth>depth+1)
				{	
					if(SearchDAG_depth(pBusSearchEngine, currentSta, curCost, busNo, (UINT8)(depth+1),MaxDepth,miniCost))
					{
						SetFlagTrue(pBusSearchEngine->fg_ST,currentSta);	
						SetFlagTrue(pBusSearchEngine->fg_ST,StaS);		
						
						if(!pBusSearchEngine->miniCost_D[StaS])
						{
							pBusSearchEngine->miniCost_D[StaS] = 
								curCost - pBusSearchEngine->miniCost_S[StaS] + pBusSearchEngine->miniCost_D[currentSta];
						}else
							if(pBusSearchEngine->miniCost_D[StaS] > curCost - pBusSearchEngine->miniCost_S[StaS] + pBusSearchEngine->miniCost_D[currentSta])
								pBusSearchEngine->miniCost_D[StaS]=curCost - pBusSearchEngine->miniCost_S[StaS] + pBusSearchEngine->miniCost_D[currentSta];
						outDegreeCnt++;
						flag = 1;
					}
				}
			}

			if(pBusSearchEngine->pData->pBus[busNo].type == 1)
			{
				curCost=cost;
				for(j=lastSpos-1; j>=0; j--)
				{
					if(curCost++>(miniCost-2 + pBusSearchEngine->exDistance))
#ifdef SAME2SAME
					{
						while(j>=0)
						{
							if(pBusSearchEngine->pData->pBus[busNo].pStation_array[j] == StaS)
								break;
							j--;
						}
						if(j < 0)
							break;
						else
						{
							curCost = cost;
							continue;
						}
					}
#else
						break;
#endif
					
					currentSta = pBusSearchEngine->pData->pBus[busNo].pStation_array[j];
#ifdef SAME2SAME
					if(currentSta == StaS)
					{
						curCost = cost;
						continue;
					}
#endif
					if(curCost != pBusSearchEngine->miniCost_S[currentSta] || pBusSearchEngine->miniTranTimes[currentSta] != depth+1 || pBusSearchEngine->miniCost_S[StaS]==0xfdfd)
						continue;
					if(pBusSearchEngine->miniCost_D[currentSta])
					{
					//Èç¹ûµ±Ç°Õ¾µÄºó¼ÌÕ¾currentStaÔÚ×î¼ÑÂ·¾¶ÉÏ
						
						if(pBusSearchEngine->miniCost_D[currentSta]+curCost <= miniCost + pBusSearchEngine->exDistance)
						{
						//µ±Ç°Õ¾StaSÔÚ×î¼ÑÂ·¾¶ÉÏ
							SetFlagTrue(pBusSearchEngine->fg_ST,currentSta);
							SetFlagTrue(pBusSearchEngine->fg_ST,StaS);
							
							if(MaxDepth == depth+1)//currentStaÄÜÖ±´ïÄ¿µÄÕ¾£¬ÇÒÔÚ×î¼ÑÂ·¾¶ÉÏ
								pBusSearchEngine->StaDataLen[currentSta] = 0xffff;
							if(!pBusSearchEngine->miniCost_D[StaS])
							{
								pBusSearchEngine->miniCost_D[StaS] = 
									curCost - pBusSearchEngine->miniCost_S[StaS] + pBusSearchEngine->miniCost_D[currentSta];
							}else
								if(pBusSearchEngine->miniCost_D[StaS] > curCost - pBusSearchEngine->miniCost_S[StaS] + pBusSearchEngine->miniCost_D[currentSta])
									pBusSearchEngine->miniCost_D[StaS]=curCost - pBusSearchEngine->miniCost_S[StaS] + pBusSearchEngine->miniCost_D[currentSta];
							//ÕÒµ½Ò»ÌõÂ·¾¶
			//				DEBUG_PRINTF("%d: %s\n",currentSta, pData->pStation[currentSta].name);
			//				DEBUG_PRINTF("%s\n", pData->pBus[busNo].name);
							outDegreeCnt++;
							flag = 1;
						}
					}
					else if(MaxDepth>depth+1)
					{	
						if(SearchDAG_depth(pBusSearchEngine, currentSta, curCost, busNo, (UINT8)(depth+1),MaxDepth,miniCost))
						{
							SetFlagTrue(pBusSearchEngine->fg_ST,currentSta);	
							SetFlagTrue(pBusSearchEngine->fg_ST,StaS);		
							
							if(!pBusSearchEngine->miniCost_D[StaS])
							{
								pBusSearchEngine->miniCost_D[StaS] = 
									curCost - pBusSearchEngine->miniCost_S[StaS] + pBusSearchEngine->miniCost_D[currentSta];
							}else
								if(pBusSearchEngine->miniCost_D[StaS] > curCost - pBusSearchEngine->miniCost_S[StaS] + pBusSearchEngine->miniCost_D[currentSta])
									pBusSearchEngine->miniCost_D[StaS]=curCost - pBusSearchEngine->miniCost_S[StaS] + pBusSearchEngine->miniCost_D[currentSta];
							outDegreeCnt++;
							flag = 1;
						}
					}
				}
			}
		}
		else
		{
			for(j=(k+1)%staCnt; j!=k; j=(j+1)%staCnt)
			{
				if(curCost++>(miniCost-2 + pBusSearchEngine->exDistance))
#ifdef SAME2SAME
				{
					while(j!=k)
					{
						if(pBusSearchEngine->pData->pBus[busNo].pStation_array[j]==StaS)
							break;
						j = (j+1)%staCnt;
					}
					if(j == k)
						break;
					else
					{
						curCost = cost;
						continue;
					}
				}
#else
					break;
#endif
				
				currentSta = pBusSearchEngine->pData->pBus[busNo].pStation_array[j];
#ifdef SAME2SAME
				if(currentSta == StaS)
				{
					curCost = cost;
					continue;
				}
#endif
				if(curCost != pBusSearchEngine->miniCost_S[currentSta] || pBusSearchEngine->miniTranTimes[currentSta] != depth+1 || pBusSearchEngine->miniCost_S[StaS]==0xfdfd)
					continue;
				if(pBusSearchEngine->miniCost_D[currentSta])
				{
				//Èç¹ûµ±Ç°Õ¾µÄºó¼ÌÕ¾currentStaÔÚ×î¼ÑÂ·¾¶ÉÏ
					
					if(pBusSearchEngine->miniCost_D[currentSta]+curCost <= miniCost + pBusSearchEngine->exDistance)
					{
					//µ±Ç°Õ¾StaSÔÚ×î¼ÑÂ·¾¶ÉÏ
						SetFlagTrue(pBusSearchEngine->fg_ST,currentSta);
						SetFlagTrue(pBusSearchEngine->fg_ST,StaS);
						
						if(MaxDepth == depth+1)//currentStaÄÜÖ±´ïÄ¿µÄÕ¾£¬ÇÒÔÚ×î¼ÑÂ·¾¶ÉÏ
							pBusSearchEngine->StaDataLen[currentSta] = 0xffff;
						if(!pBusSearchEngine->miniCost_D[StaS])
						{
							pBusSearchEngine->miniCost_D[StaS] = 
								curCost - pBusSearchEngine->miniCost_S[StaS] + pBusSearchEngine->miniCost_D[currentSta];
						}else
							if(pBusSearchEngine->miniCost_D[StaS] > curCost - pBusSearchEngine->miniCost_S[StaS] + pBusSearchEngine->miniCost_D[currentSta])
								pBusSearchEngine->miniCost_D[StaS]=curCost - pBusSearchEngine->miniCost_S[StaS] + pBusSearchEngine->miniCost_D[currentSta];
						//ÕÒµ½Ò»ÌõÂ·¾¶
		//				DEBUG_PRINTF("%d: %s\n",currentSta, pData->pStation[currentSta].name);
		//				DEBUG_PRINTF("%s\n", pData->pBus[busNo].name);
						outDegreeCnt++;
						flag = 1;
					}
				}
				else if(MaxDepth>depth+1)
				{	
					if(SearchDAG_depth(pBusSearchEngine, currentSta, curCost, busNo, (UINT8)(depth+1),MaxDepth,miniCost))
					{
						SetFlagTrue(pBusSearchEngine->fg_ST,currentSta);	
						SetFlagTrue(pBusSearchEngine->fg_ST,StaS);		
						
						if(!pBusSearchEngine->miniCost_D[StaS])
						{
							pBusSearchEngine->miniCost_D[StaS] = 
								curCost - pBusSearchEngine->miniCost_S[StaS] + pBusSearchEngine->miniCost_D[currentSta];
						}else
							if(pBusSearchEngine->miniCost_D[StaS] > curCost - pBusSearchEngine->miniCost_S[StaS] + pBusSearchEngine->miniCost_D[currentSta])
								pBusSearchEngine->miniCost_D[StaS]=curCost - pBusSearchEngine->miniCost_S[StaS] + pBusSearchEngine->miniCost_D[currentSta];
						outDegreeCnt++;
						flag = 1;
					}
				}
			}
		}
		if(flag)
		{//µ±Ç°³µ´ÎÔÚ×î¼ÑÂ·¾¶ÉÏ
			SetFlagTrue(pBusSearchEngine->fg_BL, busNo);
			acBusCnt++;
		}
	}
	if(outDegreeCnt && acBusCnt)
	{
		//±£´æÃ¿¸öÔÚ×î¼ÑÂ·¾¶ÉÏµÄÕ¾ËùÕ¼ÓÃµÄ¿Õ¼ä
		pBusSearchEngine->StaDataLen[StaS]=pBusSearchEngine->DataSize;
		pBusSearchEngine->DataSize += (2+acBusCnt*2+outDegreeCnt*3);
		return pBusSearchEngine->DataSize;
	}
	else
	{
		pBusSearchEngine->miniCost_S[StaS]=0xfdfd;//ÒÑ¾­È·¶¨²»ÔÚ×î¼ÑÂ·ÏßÉÏ
		return 0;
	}
}


#define  ADD_SOULUTION(a) {pBusSearchEngine->solutionData[pBusSearchEngine->StaDataLen[StaS]+StaDataLen_offset++]=(a);pBusSearchEngine->DataLen2++;}
//(StaS ((NextStaOffset CurBusLinePos_NextSta Cost_StaS_To_NextSta)  [nNextStation]		busNo BLFLAG)  [nBusLine]		ENDFLAG)  [nStation]
//(1		((	3	[nNextStation])	2	)[nBusLine]	1)[nStation]
//(1		+	3*n1	+	2*n2	+1)
static void SearchDAG_depth4Bulid(
	struct busSearchEngine* const pBusSearchEngine,
	UINT16 StaS,
	UINT16 cost,
	UINT16 preBusNo,
	UINT8 depth,
	const UINT8 MaxDepth,
	const UINT16 miniCost
	)
{
	int i,j,k, lastSpos;
	UINT16 busCnt=pBusSearchEngine->pData->pStation[StaS].bus_count;
	UINT16* pBus_array=pBusSearchEngine->pData->pStation[StaS].pBus_array;
	UINT16 busNo, staCnt, currentSta, curCost;
	UINT16 outDegreeCnt=0, acBusCnt=0;
	UINT16 flag, StaDataLen_offset=0;
	pBusSearchEngine->exCnt++;

	ADD_SOULUTION(StaS);
		
	for(i=0; i<busCnt; i++)
	{
		busNo=pBus_array[i];
		if(!GetFlag(pBusSearchEngine->fg_BL, busNo))
			continue;
		if(preBusNo == busNo)//Ò»¶¨ÒªÓÐ£¬²»È»¿ÉÄÜ»áÖ´ÐÐacBusCnt++;
			continue;
		flag=0;
		k=0;while(pBusSearchEngine->pData->pBus[busNo].pStation_array[k]!=StaS) k++;
		staCnt=pBusSearchEngine->pData->pBus[busNo].station_count;
		curCost=cost;
		if(pBusSearchEngine->pData->pBus[busNo].type != 0)
		{
			lastSpos = k-1;
			for(j=k; j<staCnt; j++)
			{
				if(curCost++>miniCost-2 + pBusSearchEngine->exDistance)
#ifdef SAME2SAME
				{
					while(j<staCnt)
					{ 
						if(pBusSearchEngine->pData->pBus[busNo].pStation_array[j]==StaS)
							break;
						j++;
					}
					if(j >= staCnt)
						break;
					else
					{
						curCost = cost;
						continue;
					}
				}
#else
					break;
#endif
				
				currentSta = pBusSearchEngine->pData->pBus[busNo].pStation_array[j];
#ifdef SAME2SAME
				if(currentSta == StaS)
				{
					curCost = cost;
					lastSpos = j;
					continue;
				}
#endif
				if(!GetFlag(pBusSearchEngine->fg_ST, currentSta))
					continue;
				if(curCost != pBusSearchEngine->miniCost_S[currentSta] || pBusSearchEngine->miniTranTimes[currentSta] != depth+1)
					continue;

				//ÕÒµ½Ò»ÌõÂ·¾¶
				ADD_SOULUTION(pBusSearchEngine->StaDataLen[currentSta]);
		//		DEBUG_PRINTF("%d\t",StaDataLen[currentSta]);
				ADD_SOULUTION(j);
				ADD_SOULUTION(curCost-cost);
				outDegreeCnt++;
				flag = 1;

				//±éÀúºó¼ÌÕ¾
				if(!GetFlag(pBusSearchEngine->fg_STE, currentSta) && (MaxDepth > depth+1))
				{
					SetFlagTrue(pBusSearchEngine->fg_STE, currentSta);
					SearchDAG_depth4Bulid(pBusSearchEngine, currentSta, curCost, busNo, (UINT8)(depth+1),MaxDepth,miniCost);
				}

			}
			if(pBusSearchEngine->pData->pBus[busNo].type == 1)
			{
				curCost=cost;
				for(j=lastSpos-1; j>=0; j--)
				{
					if(curCost++>miniCost-2 + pBusSearchEngine->exDistance)
#ifdef SAME2SAME
					{
						while(j>=0)
						{
							if(pBusSearchEngine->pData->pBus[busNo].pStation_array[j] == StaS)
								break;
							j--;
						}
						if(j < 0)
							break;
						else
						{
							curCost = cost;
							continue;
						}
					}
#else
						break;
#endif
					
					currentSta = pBusSearchEngine->pData->pBus[busNo].pStation_array[j];
#ifdef SAME2SAME
					if(currentSta == StaS)
					{
						curCost = cost;
						continue;
					}
#endif
					if(!GetFlag(pBusSearchEngine->fg_ST, currentSta))
						continue;
					if(curCost != pBusSearchEngine->miniCost_S[currentSta] || pBusSearchEngine->miniTranTimes[currentSta] != depth+1)
						continue;

					//ÕÒµ½Ò»ÌõÂ·¾¶
					ADD_SOULUTION(pBusSearchEngine->StaDataLen[currentSta]);
			//		DEBUG_PRINTF("%d\t",StaDataLen[currentSta]);
					ADD_SOULUTION(j);
					ADD_SOULUTION(curCost-cost);
					outDegreeCnt++;
					flag = 1;

					//±éÀúºó¼ÌÕ¾
					if(!GetFlag(pBusSearchEngine->fg_STE, currentSta) && (MaxDepth > depth+1))
					{
						SetFlagTrue(pBusSearchEngine->fg_STE, currentSta);
						SearchDAG_depth4Bulid(pBusSearchEngine, currentSta, curCost, busNo, (UINT8)(depth+1),MaxDepth,miniCost);
					}

				}
			}
		}
		else
		{
			for(j=(k+1)%staCnt; j!=k; j=(j+1)%staCnt)
			{
				if(curCost++>miniCost-2 + pBusSearchEngine->exDistance)
#ifdef SAME2SAME
				{
					while(j!=k)
					{
						if(pBusSearchEngine->pData->pBus[busNo].pStation_array[j]==StaS)
							break;
						j = (j+1)%staCnt;
					}
					if(j == k)
						break;
					else
					{
						curCost = cost;
						continue;
					}
				}
#else
					break;
#endif
				
				currentSta = pBusSearchEngine->pData->pBus[busNo].pStation_array[j];
#ifdef SAME2SAME
				if(currentSta == StaS)
				{
					curCost = cost;
					continue;
				}
#endif
				if(!GetFlag(pBusSearchEngine->fg_ST, currentSta))
					continue;
				if(curCost != pBusSearchEngine->miniCost_S[currentSta] || pBusSearchEngine->miniTranTimes[currentSta] != depth+1)
					continue;

				//ÕÒµ½Ò»ÌõÂ·¾¶
				ADD_SOULUTION(pBusSearchEngine->StaDataLen[currentSta]);
		//		DEBUG_PRINTF("%d\t",StaDataLen[currentSta]);
				ADD_SOULUTION(j);
				ADD_SOULUTION(curCost-cost);
				outDegreeCnt++;
				flag = 1;

				//±éÀúºó¼ÌÕ¾
				if(!GetFlag(pBusSearchEngine->fg_STE, currentSta) && (MaxDepth > depth+1))
				{
					SetFlagTrue(pBusSearchEngine->fg_STE, currentSta);
					SearchDAG_depth4Bulid(pBusSearchEngine, currentSta, curCost, busNo, (UINT8)(depth+1),MaxDepth,miniCost);
				}

			}
		}
		if(flag)
		{
			ADD_SOULUTION(busNo);
			ADD_SOULUTION(BLFLAG);
			acBusCnt++;
		}
		
	}
#if 0
	if(acBusCnt != 0 && outDegreeCnt != 0)
	{
		if(StaDataLen[StaS]!=DataSize3)
		{
			DEBUG_PRINTF("StaDataLen ERROR!");
		}
		DataSize3 += (2+acBusCnt*2+outDegreeCnt*3);
	}
#endif
	ADD_SOULUTION(ENDFLAG);
//	DataLen2 += (2+acBusCnt*2+outDegreeCnt*2);
}
/*solutionData 
	Head:	solutionDataLen 	1			words
			StaS 			1			words
			StaD 			1			words
			MaxDepth 		1			words
			miniCost			1			words
			solutionData[Stas]	1			words
	Body:	BodyLen			1			words
			MainSolutionData	BodyLen		words
	Strings:	StringDataLen		1			words
			StringIndexTable	strCnt		words
			Strings			strLen 		bytes
*/
//static UINT CompleteSolutionStream(struct busSearchEngine* const pBusSearchEngine, UINT16* pSolutionData);
//static UINT ReviewSolutionStream(struct busSearchEngine* pBusSearchEngine, UINT16* pSolutionData);
static UINT BuildSolutionStream(
	struct busSearchEngine* const pBusSearchEngine,
	UINT16 StaS, 				//µ±Ç°Õ¾
	UINT16 cost, 					//µ±Ç°Õ¾µÄ´ú¼Û
	UINT16 preBusNo,
	UINT8 depth,
	const UINT8 MaxDepth,
	const UINT16 miniCost,		//³ö·¢Õ¾µ½Ä¿µÄÕ¾µÄ×îÐ¡´ú¼Û
	const UINT16 StaD
	)//UINT16*
{
	int i, j, tempOffset=0, stacnt, curcost, k, tempOffsetcnt=0, len,lastSpos;
	UINT16* pBus, *pStation;
	
	UINT16* newArray, *pBusAray_D = pBusSearchEngine->pData->pStation[StaD].pBus_array;
	UINT16	pBusAray_D_cnt = pBusSearchEngine->pData->pStation[StaD].bus_count;
	SoultionHead* pSoultionHead=(SoultionHead*)pBusSearchEngine->solutionData;
	pSoultionHead->stationCnt = 0;
	pSoultionHead->busCnt = 0;
////////////////////////////////////////////////////////////////////////////////////
	
	MEMSET(pBusSearchEngine->fg_BL, 0, ((pBusSearchEngine->pData->bus_count+7)/8));
	MEMSET(pBusSearchEngine->fg_ST, 0, ((pBusSearchEngine->pData->station_count+7)/8));
	MEMSET(pBusSearchEngine->StaDataLen, 0, pBusSearchEngine->pData->station_count*sizeof(UINT16));
	pBusSearchEngine->DataSize=sizeof(SoultionHead)/sizeof(UINT16);//SearchDAG_depth º¯ÊýµÄ³õÊ¼»¯
	pBusSearchEngine->exCnt = 0;
	if((len = SearchDAG_depth(pBusSearchEngine, StaS, cost, preBusNo, depth, MaxDepth, miniCost)) == 0)
	{
		DEBUG_PRINTF("ERROR! k== 0, S = %d, D = %d\nLine:%d\n", StaS, StaD, __LINE__);
	//	ASSERT(0);
	}
////////////////////////////////////////////////////////////////////////////////////
	pBusSearchEngine->DataLen2 = sizeof(SoultionHead)/sizeof(UINT16);
	if(pBusSearchEngine->tempArray == NULL)
		pBusSearchEngine->tempArray = (UINT16*)MALLOC(pBusSearchEngine->MaxDirOffset*sizeof(UINT16));
	MEMSET(pBusSearchEngine->fg_STE, 0, ((pBusSearchEngine->pData->station_count+7)/8));
	
/////////////////////////////////////////////////////////////
/************sta Nbus minicost bus0 bus1 ... busN***************************/
	for(i=0; i<pBusSearchEngine->pData->station_count; i++)
	{
		UINT16 tempPos, tempK, v;
		if(pBusSearchEngine->StaDataLen[i] == 0xffff)
		{//ÔÚ×î¼ÑÂ·¾¶ÉÏÇÒÖ±´ïÄ¿µÄÕ¾
			pBus = pBusSearchEngine->pData->pStation[i].pBus_array;
			tempPos = tempOffsetcnt;
			tempOffsetcnt+=3;
			tempOffset = 3;
			if(tempOffsetcnt > pBusSearchEngine->MaxDirOffset)
			{
				UINT16 temp = pBusSearchEngine->MaxDirOffset;
				while(tempOffsetcnt>pBusSearchEngine->MaxDirOffset)
					pBusSearchEngine->MaxDirOffset = pBusSearchEngine->MaxDirOffset*2;
				newArray = (UINT16*)MALLOC(pBusSearchEngine->MaxDirOffset*sizeof(UINT16));
				MEMCPY(newArray, pBusSearchEngine->tempArray, temp*sizeof(UINT16));
				DEBUG_PRINTF("line:%d, length = %d\n", __LINE__, temp);
				FREE(pBusSearchEngine->tempArray);
				pBusSearchEngine->tempArray = newArray;
			}
			pBusSearchEngine->tempArray[tempPos] = i;
			pBusSearchEngine->tempArray[tempPos+1]=0;
			pBusSearchEngine->tempArray[tempPos+2]=pBusSearchEngine->miniCost_D[i];
			for(k = 0; k < pBusSearchEngine->pData->pStation[i].bus_count; k++)
			{
				for(v=0;v<pBusAray_D_cnt;v++)
					if(pBusAray_D[v] == pBus[k])
						break;
				if(v == pBusAray_D_cnt)
					continue;
					
				stacnt = pBusSearchEngine->pData->pBus[pBus[k]].station_count;
				pStation = pBusSearchEngine->pData->pBus[pBus[k]].pStation_array;
				curcost = 0;
				j = 0;
				tempK = 0;
				
				while(pStation[tempK] != i && tempK<stacnt) tempK++;
				if(tempK>=stacnt)
					DEBUG_PRINTF("tempK>=stacnt line:%d\n", __LINE__);
				lastSpos = tempK;
				if(pBusSearchEngine->pData->pBus[pBus[k]].type != 0)
				{
					for(j = tempK+1 ; j < stacnt; j++)
					{
						if(pStation[j] == i)
						{
							curcost = 0;
							lastSpos = j;
							continue;
						}
						else
						{
							curcost++;
							if( pStation[j] == StaD && curcost == pBusSearchEngine->miniCost_D[i])
							{
								tempOffsetcnt++;
								tempOffset++;
								if(tempOffsetcnt > pBusSearchEngine->MaxDirOffset)
								{
									UINT16 temp = pBusSearchEngine->MaxDirOffset;
									while(tempOffsetcnt>pBusSearchEngine->MaxDirOffset)
										pBusSearchEngine->MaxDirOffset = pBusSearchEngine->MaxDirOffset*2;
									newArray = (UINT16*)MALLOC(pBusSearchEngine->MaxDirOffset*sizeof(UINT16));
									MEMCPY(newArray, pBusSearchEngine->tempArray, temp*sizeof(UINT16));
									DEBUG_PRINTF("line:%d, length = %d\n", __LINE__, temp);
									FREE(pBusSearchEngine->tempArray);
									pBusSearchEngine->tempArray = newArray;
								}
								pBusSearchEngine->tempArray[tempOffsetcnt-1]= pBus[k];
								pBusSearchEngine->tempArray[tempPos+1]++;
								break;
							}
						}
					}

					if(pBusSearchEngine->pData->pBus[pBus[k]].type == 1)
					{
						curcost = 0;
						for(j = lastSpos-1 ; j >=0; j--)
						{
							if(pStation[j] == i)
							{
								curcost = 0;
								continue;
							}
							else
							{
								curcost++;
								if( pStation[j] == StaD && curcost == pBusSearchEngine->miniCost_D[i])
								{
									tempOffsetcnt++;
									tempOffset++;
									if(tempOffsetcnt > pBusSearchEngine->MaxDirOffset)
									{
										UINT16 temp = pBusSearchEngine->MaxDirOffset;
										while(tempOffsetcnt>pBusSearchEngine->MaxDirOffset)
											pBusSearchEngine->MaxDirOffset = pBusSearchEngine->MaxDirOffset*2;
										newArray = (UINT16*)MALLOC(pBusSearchEngine->MaxDirOffset*sizeof(UINT16));
										MEMCPY(newArray, pBusSearchEngine->tempArray, temp*sizeof(UINT16));
										DEBUG_PRINTF("line:%d, length = %d\n", __LINE__, temp);
										FREE(pBusSearchEngine->tempArray);
										pBusSearchEngine->tempArray = newArray;
									}
									pBusSearchEngine->tempArray[tempOffsetcnt-1]= pBus[k];
									pBusSearchEngine->tempArray[tempPos+1]++;
									break;
								}
							}
						}
					}
				}
				else
				{
					for(j = tempK+1; j != tempK; j=(j+1)%stacnt)
					{
						if(pStation[j] == i)
						{
							curcost = 0;
							continue;
						}
						else
						{
							curcost++;
							if( pStation[j] == StaD && curcost == pBusSearchEngine->miniCost_D[i])
							{
								tempOffsetcnt++;
								tempOffset++;
								if(tempOffsetcnt > pBusSearchEngine->MaxDirOffset)
								{
									UINT16 temp = pBusSearchEngine->MaxDirOffset;
									while(tempOffsetcnt>pBusSearchEngine->MaxDirOffset)
										pBusSearchEngine->MaxDirOffset = pBusSearchEngine->MaxDirOffset*2;
									newArray = (UINT16*)MALLOC(pBusSearchEngine->MaxDirOffset*sizeof(UINT16));
									MEMCPY(newArray, pBusSearchEngine->tempArray, temp*sizeof(UINT16));
									DEBUG_PRINTF("line:%d, length = %d\n", __LINE__, temp);
									FREE(pBusSearchEngine->tempArray);
									pBusSearchEngine->tempArray = newArray;
								}
								pBusSearchEngine->tempArray[tempOffsetcnt-1]= pBus[k];
								pBusSearchEngine->tempArray[tempPos+1]++;
								break;
							}
						}
					}
				}
			}
			if(tempOffset == 3 )
			{
				DEBUG_PRINTF("ERROR--sta Nbus bus0 bus1 ... busN  S = %d D = %d\nLine: %d\n", StaS, StaD, __LINE__);
			}
			pBusSearchEngine->StaDataLen[i] = pBusSearchEngine->DataSize;// + tempOffset;
			pBusSearchEngine->DataSize += tempOffset;
		}
		
	}
	
	if(pBusSearchEngine->DataSize>pBusSearchEngine->solutionDataLen)
	{
		UINT16 *tempP = NULL, tempLen = pBusSearchEngine->solutionDataLen;
		while(pBusSearchEngine->solutionDataLen < pBusSearchEngine->DataSize)
			pBusSearchEngine->solutionDataLen = pBusSearchEngine->solutionDataLen*2;
		tempP = (UINT16*)MALLOC(pBusSearchEngine->solutionDataLen*sizeof(UINT16));
		MEMCPY(tempP, pBusSearchEngine->solutionData, tempLen*sizeof(UINT16));
		DEBUG_PRINTF("line:%d, length = %d\n", __LINE__, tempLen);
		MYFREE(pBusSearchEngine->solutionData);
		pBusSearchEngine->solutionData = tempP;
		pSoultionHead = (SoultionHead*)pBusSearchEngine->solutionData;
	}
	
	MEMCPY(pBusSearchEngine->solutionData+pBusSearchEngine->DataSize-tempOffsetcnt, pBusSearchEngine->tempArray, tempOffsetcnt*sizeof(UINT16));
	if( pBusSearchEngine->MaxDirOffset<tempOffsetcnt)
	{
		DEBUG_PRINTF("ERROR--MaxDirOffset %d<tempOffsetcnt %d\nLine:%d",pBusSearchEngine->MaxDirOffset, tempOffsetcnt, __LINE__);
	}
//	DEBUG_PRINTF("MaxDirOffset=%d	tempOffsetcnt=%d\n",MaxDirOffset, tempOffsetcnt);
/////////////////////////////////////////////////////////////
	
//	DataSize3 = 0;
	pBusSearchEngine->SearchDAG_depth4Bulid(pBusSearchEngine, StaS, cost, preBusNo, depth, MaxDepth, miniCost);
	if(pBusSearchEngine->DataLen2!=pBusSearchEngine->DataSize-tempOffsetcnt)
		DEBUG_PRINTF("ERROR SIZE!!!\nLine:%d\n", __LINE__);
	pSoultionHead->solutionData_len = 0;
	pSoultionHead->body_len = pBusSearchEngine->DataSize;
	pSoultionHead->station_S = StaS;
	pSoultionHead->station_D = StaD;
	pSoultionHead->miniCost = miniCost;
	pSoultionHead->station_S_offset = pBusSearchEngine->StaDataLen[StaS];
	pSoultionHead->transfer_times = MaxDepth;
	pSoultionHead->string_len = 0;
	
	pBusSearchEngine->CompleteSolutionStream(pBusSearchEngine, pBusSearchEngine->solutionData);
	
	return (UINT)pBusSearchEngine->solutionData;
}
static UINT SortSolutionStation(struct busSearchEngine* const pBusSearchEngine, UINT16* pSolutionData);
static UINT CompleteSolutionStream(struct busSearchEngine* const pBusSearchEngine, UINT16* pSolutionData) //SoultionHead*
{
	SoultionHead* pSoultionHead=(SoultionHead*)pBusSearchEngine->solutionData;
	UINT16* pIndex = pBusSearchEngine->pBusQ;
	UINT16* pQueue = pBusSearchEngine->miniCost_D;
	UINT16 queue_top = 1;
	UINT16 queue_bot=0;
	UINT16 strLen=0, tempStrLen;
	if(pSolutionData == NULL || pBusSearchEngine->pData == NULL)
		return (UINT)NULL;
	pQueue[0] = pSoultionHead->station_S_offset;
	pSoultionHead->solutionData_len = pSoultionHead->body_len*sizeof(UINT16);
	pSoultionHead->stationCnt = 0;
//	pSoultionHead->pSolutionData = (UINT8*)pSolutionData + sizeof(SoultionHead);
	pSoultionHead->pString = (UINT8*)(pBusSearchEngine->solutionData + pSoultionHead->body_len);
	MEMSET(pIndex, 0xff, pBusSearchEngine->pData->bus_count*sizeof(UINT16));
/****************************************************************************/
	tempStrLen = strlen(pBusSearchEngine->pData->pStation[pSoultionHead->station_D].name)+1;
	pSoultionHead->solutionData_len+=tempStrLen;
	pSoultionHead->string_len += tempStrLen;
	if(pSoultionHead->solutionData_len>pBusSearchEngine->solutionDataLen*sizeof(UINT16))
	{
		UINT16 *tempP = NULL, tempLen = pBusSearchEngine->solutionDataLen;
		while(pBusSearchEngine->solutionDataLen*sizeof(UINT16) < pSoultionHead->solutionData_len)
			pBusSearchEngine->solutionDataLen = pBusSearchEngine->solutionDataLen*2;
		
		tempP = (UINT16*)MALLOC(pBusSearchEngine->solutionDataLen*sizeof(UINT16));
		MEMCPY(tempP, pBusSearchEngine->solutionData, tempLen*sizeof(UINT16));
		DEBUG_PRINTF("line:%d, length = %d\n", __LINE__, tempLen);
		MYFREE(pBusSearchEngine->solutionData);
		pBusSearchEngine->solutionData = tempP;
		pSoultionHead=(SoultionHead*)pBusSearchEngine->solutionData;
		pSoultionHead->pString = (UINT8*)(pBusSearchEngine->solutionData + pSoultionHead->body_len);
	}
	strcpy((char*)pSoultionHead->pString+strLen,(char*)pBusSearchEngine->pData->pStation[pSoultionHead->station_D].name);
	pSoultionHead->station_D = strLen;
	strLen +=  tempStrLen;
/****************************************************************************/
	{
		while(queue_top!=queue_bot)
		{
			UINT16 sta_offset, tempOffset, nextOffset, i, busNo, j, staCur;
			sta_offset = pQueue[queue_bot++];
			staCur = pBusSearchEngine->solutionData[sta_offset];
			

			pBusSearchEngine->solutionData[sta_offset] = strLen;//Ìæ»»Ë÷Òý,Ö±½Ó´æÃû³ÆµÄÆ«ÒÆÁ¿
			
			tempStrLen = strlen(pBusSearchEngine->pData->pStation[staCur].name)+1;
			pSoultionHead->solutionData_len+=tempStrLen;
			pSoultionHead->string_len += tempStrLen;
			
			if(pSoultionHead->solutionData_len>pBusSearchEngine->solutionDataLen*sizeof(UINT16))
			{
				UINT16 *tempP = NULL, tempLen = pBusSearchEngine->solutionDataLen;
				while(pBusSearchEngine->solutionDataLen*sizeof(UINT16) < pSoultionHead->solutionData_len)
					pBusSearchEngine->solutionDataLen = pBusSearchEngine->solutionDataLen*2;
				
				tempP = (UINT16*)MALLOC(pBusSearchEngine->solutionDataLen*sizeof(UINT16));
				MEMCPY(tempP, pBusSearchEngine->solutionData, tempLen*sizeof(UINT16));
				DEBUG_PRINTF("line:%d, length = %d\n", __LINE__, tempLen);
				MYFREE(pBusSearchEngine->solutionData);
				pBusSearchEngine->solutionData = tempP;
				pSoultionHead=(SoultionHead*)pBusSearchEngine->solutionData;
				pSoultionHead->pString = (UINT8*)(pBusSearchEngine->solutionData + pSoultionHead->body_len);
			}
			strcpy((char*)pSoultionHead->pString+strLen, (char*)pBusSearchEngine->pData->pStation[staCur].name);
			strLen +=  tempStrLen;
			
			if(pBusSearchEngine->miniTranTimes[staCur]<pSoultionHead->transfer_times)
			{
				tempOffset = sta_offset;
				do
				{
					i=0;
					do
					{
						nextOffset = pBusSearchEngine->solutionData[tempOffset+i*3+1];
						for(j=0;j<queue_top;j++)
						{
							if(nextOffset == pQueue[j])
								break;
						}
						if(j == queue_top)
						{
							pQueue[queue_top++] = nextOffset;
						}
						i++;
					}while( pBusSearchEngine->solutionData[tempOffset + i*3 +2] != BLFLAG);
			/*************************save bus name***************************************************/		
					busNo = pBusSearchEngine->solutionData[tempOffset + i*3 +1];
					if(pIndex[busNo] == 0xffff)
					{
						tempStrLen = strlen(pBusSearchEngine->pData->pBus[busNo].name)+1;
						pSoultionHead->solutionData_len+=tempStrLen;
						pSoultionHead->string_len += tempStrLen;
						
						if(pSoultionHead->solutionData_len>pBusSearchEngine->solutionDataLen*sizeof(UINT16))
						{
							UINT16 *tempP = NULL, tempLen = pBusSearchEngine->solutionDataLen;
							while(pBusSearchEngine->solutionDataLen*sizeof(UINT16) < pSoultionHead->solutionData_len)
								pBusSearchEngine->solutionDataLen = pBusSearchEngine->solutionDataLen*2;
							
							tempP = (UINT16*)MALLOC(pBusSearchEngine->solutionDataLen*sizeof(UINT16));
							MEMCPY(tempP, pBusSearchEngine->solutionData, tempLen*sizeof(UINT16));
							DEBUG_PRINTF("line:%d, length = %d\n", __LINE__, tempLen);
							MYFREE(pBusSearchEngine->solutionData);
							pBusSearchEngine->solutionData = tempP;
							pSoultionHead=(SoultionHead*)pBusSearchEngine->solutionData;
							pSoultionHead->pString = (UINT8*)(pBusSearchEngine->solutionData + pSoultionHead->body_len);
						}
						strcpy((char*)pSoultionHead->pString+strLen, (char*)pBusSearchEngine->pData->pBus[busNo].name);
						pIndex[busNo] = strLen;
						strLen +=  tempStrLen;
					}
					pBusSearchEngine->solutionData[tempOffset + i*3 +1] = pIndex[busNo];
			/*************************save bus name***************************************************/		
					tempOffset+=i*3 +2;
				}while(pBusSearchEngine->solutionData[tempOffset+1]!=ENDFLAG);
			}
			else
			{/*************************save bus name***************************************************/	
				if(pBusSearchEngine->miniTranTimes[staCur] == pSoultionHead->transfer_times)
				{
					for(i = 0;i<pBusSearchEngine->solutionData[sta_offset+1];i++)
					{
						busNo = pBusSearchEngine->solutionData[sta_offset + i +3];
						if(pIndex[busNo] == 0xffff)
						{
							tempStrLen = strlen(pBusSearchEngine->pData->pBus[busNo].name)+1;
							pSoultionHead->solutionData_len+=tempStrLen;
							pSoultionHead->string_len += tempStrLen;
							
							if(pSoultionHead->solutionData_len>pBusSearchEngine->solutionDataLen*sizeof(UINT16))
							{
								UINT16 *tempP = NULL, tempLen = pBusSearchEngine->solutionDataLen;
								while(pBusSearchEngine->solutionDataLen*sizeof(UINT16) < pSoultionHead->solutionData_len)
									pBusSearchEngine->solutionDataLen = pBusSearchEngine->solutionDataLen*2;
								
								tempP = (UINT16*)MALLOC(pBusSearchEngine->solutionDataLen*sizeof(UINT16));
								MEMCPY(tempP, pBusSearchEngine->solutionData, tempLen*sizeof(UINT16));
								DEBUG_PRINTF("line:%d, length = %d\n", __LINE__, tempLen);
								MYFREE(pBusSearchEngine->solutionData);
								pBusSearchEngine->solutionData = tempP;
								pSoultionHead=(SoultionHead*)pBusSearchEngine->solutionData;
								pSoultionHead->pString = (UINT8*)(pBusSearchEngine->solutionData + pSoultionHead->body_len);
							}
							strcpy((char*)pSoultionHead->pString+strLen, (char*)pBusSearchEngine->pData->pBus[busNo].name);
							pIndex[busNo] = strLen;
							strLen +=  tempStrLen;
						}
						pBusSearchEngine->solutionData[sta_offset + i +3] = pIndex[busNo];
					}
				}
				
			}/*************************save bus name***************************************************/	
		}

	}
	if(pBusSearchEngine->exDistance >0)
		SortSolutionStation(pBusSearchEngine, pSolutionData);
	return (UINT)pSoultionHead;
}
#define REALLOC(p, len, curlen)\
	if(curlen >= len)\
	{\
		int oldlen = len;\
		char* newp = NULL;\
		while(curlen >= len)\
			len = len*2;\
		newp = (char*)malloc(len*sizeof(char));\
		MEMCPY(newp, p, oldlen);\
		FREE(p);\
		p = newp;\
	}
static UINT ReviewSolutionStream(struct busSearchEngine* const pBusSearchEngine, UINT16* pSolutionData)//char*
{
	int strLen = 0, temLen = 0, space = 0;
	SoultionHead* pSoultionHead=(SoultionHead*)pBusSearchEngine->solutionData;
	UINT16* pQueue = pBusSearchEngine->pStaInQueue;
	UINT16 queue_top = 1;
	UINT16 queue_bot=0;
	UINT8* pQueueTrTimes = (UINT8*)pBusSearchEngine->miniTranTimes;
	
	if(pSolutionData == NULL)
	{
		MYFREE(pBusSearchEngine->output);
		return (UINT)NULL;
	}
	if(pBusSearchEngine->output == NULL)
		pBusSearchEngine->output = (char*)MALLOC(pBusSearchEngine->outputLen*sizeof(char));
	pQueue[0] = pSoultionHead->station_S_offset;
	pQueueTrTimes[0]=0;
	
	while(queue_top!=queue_bot)
	{
		UINT16 sta_offset, tempOffset, nextOffset, i, l, curTrTime;
		curTrTime = pQueueTrTimes[queue_bot];
		sta_offset = pQueue[queue_bot++];
		if(curTrTime == 0)
			sprintf(pBusSearchEngine->tempString, "��%s ����:", pSoultionHead->pString+pSolutionData[sta_offset]);
		else
		{
			sprintf(pBusSearchEngine->tempString, "\r\n");
			temLen = strlen(pBusSearchEngine->tempString);
			REALLOC(pBusSearchEngine->output, pBusSearchEngine->outputLen, strLen+temLen);
			MEMCPY(pBusSearchEngine->output+strLen, pBusSearchEngine->tempString, temLen);
			strLen+=temLen;
			for(space=0;space<curTrTime;space++)
			{
				sprintf(pBusSearchEngine->tempString, "    ");
				temLen = strlen(pBusSearchEngine->tempString);
				REALLOC(pBusSearchEngine->output, pBusSearchEngine->outputLen, strLen+temLen);
				MEMCPY(pBusSearchEngine->output+strLen, pBusSearchEngine->tempString, temLen);
				strLen+=temLen;
			}
			sprintf(pBusSearchEngine->tempString, "�� %s ��%d�λ���:", pSoultionHead->pString+pSolutionData[sta_offset], curTrTime);
		}
		temLen = strlen(pBusSearchEngine->tempString);
		REALLOC(pBusSearchEngine->output, pBusSearchEngine->outputLen, strLen+temLen);
		MEMCPY(pBusSearchEngine->output+strLen, pBusSearchEngine->tempString, temLen);
		strLen+=temLen;

		if(curTrTime<pSoultionHead->transfer_times)
		{
		
			UINT16 j = 0;
			tempOffset = sta_offset;
			do
			{
				i=0;
				j++;
		/*************************view bus name***************************************************/	
				do
				{
					i++;
				}while(pSolutionData[tempOffset + i*3 +2] != BLFLAG);
				sprintf(pBusSearchEngine->tempString, "\r\n");
				temLen = strlen(pBusSearchEngine->tempString);
				REALLOC(pBusSearchEngine->output, pBusSearchEngine->outputLen, strLen+temLen);
				MEMCPY(pBusSearchEngine->output+strLen, pBusSearchEngine->tempString, temLen);
				strLen+=temLen;
				for(space=0;space<curTrTime;space++)
				{
					sprintf(pBusSearchEngine->tempString, "    ");
					temLen = strlen(pBusSearchEngine->tempString);
					REALLOC(pBusSearchEngine->output, pBusSearchEngine->outputLen, strLen+temLen);
					MEMCPY(pBusSearchEngine->output+strLen, pBusSearchEngine->tempString, temLen);
					strLen+=temLen;
				}
				sprintf(pBusSearchEngine->tempString, "    �� %s ��:\r\n", pSoultionHead->pString+pSolutionData[tempOffset + i*3 +1]);
				temLen = strlen(pBusSearchEngine->tempString);
				REALLOC(pBusSearchEngine->output, pBusSearchEngine->outputLen, strLen+temLen);
				MEMCPY(pBusSearchEngine->output+strLen, pBusSearchEngine->tempString, temLen);
				strLen+=temLen;
				for(space=0;space<curTrTime+1;space++)
				{
					sprintf(pBusSearchEngine->tempString, "    ");
					temLen = strlen(pBusSearchEngine->tempString);
					REALLOC(pBusSearchEngine->output, pBusSearchEngine->outputLen, strLen+temLen);
					MEMCPY(pBusSearchEngine->output+strLen, pBusSearchEngine->tempString, temLen);
					strLen+=temLen;
				}
		/*************************save bus name***************************************************/	
				i=0;
				do
				{
					nextOffset = pSolutionData[tempOffset+i*3+1];
					sprintf(pBusSearchEngine->tempString, "%s(%d)  ", pSoultionHead->pString+pSolutionData[nextOffset], pSolutionData[tempOffset+i*3+3]);
					temLen = strlen(pBusSearchEngine->tempString);
					REALLOC(pBusSearchEngine->output, pBusSearchEngine->outputLen, strLen+temLen);
					MEMCPY(pBusSearchEngine->output+strLen, pBusSearchEngine->tempString, temLen);
					strLen+=temLen;

					for(l=0;l<queue_top;l++)
					{
						if(nextOffset == pQueue[l])
							break;
					}
					if(l == queue_top)
					{
						pQueueTrTimes[queue_top] = curTrTime+1;
						pQueue[queue_top++] = nextOffset;
					}
					i++;
				}while( pSolutionData[tempOffset + i*3 +2] != BLFLAG);
			
				tempOffset+=i*3 +2;
			}while(pSolutionData[tempOffset+1]!=ENDFLAG);
			sprintf(pBusSearchEngine->tempString, "\r\n");
			temLen = strlen(pBusSearchEngine->tempString);
			REALLOC(pBusSearchEngine->output, pBusSearchEngine->outputLen, strLen+temLen);
			MEMCPY(pBusSearchEngine->output+strLen, pBusSearchEngine->tempString, temLen);
			strLen+=temLen;
		}
		else
		{/*************************save bus name***************************************************/	
			if(curTrTime == pSoultionHead->transfer_times)
			{
				
				sprintf(pBusSearchEngine->tempString, "\r\n");
				temLen = strlen(pBusSearchEngine->tempString);
				REALLOC(pBusSearchEngine->output, pBusSearchEngine->outputLen, strLen+temLen);
				MEMCPY(pBusSearchEngine->output+strLen, pBusSearchEngine->tempString, temLen);
				strLen+=temLen;
				for(space=0;space<curTrTime;space++)
				{
					sprintf(pBusSearchEngine->tempString, "    ");
					temLen = strlen(pBusSearchEngine->tempString);
					REALLOC(pBusSearchEngine->output, pBusSearchEngine->outputLen, strLen+temLen);
					MEMCPY(pBusSearchEngine->output+strLen, pBusSearchEngine->tempString, temLen);
					strLen+=temLen;
				}
				sprintf(pBusSearchEngine->tempString, "    �� ");
				temLen = strlen(pBusSearchEngine->tempString);
				REALLOC(pBusSearchEngine->output, pBusSearchEngine->outputLen, strLen+temLen);
				MEMCPY(pBusSearchEngine->output+strLen, pBusSearchEngine->tempString, temLen);
				strLen+=temLen;
				for(i = 0;i<pSolutionData[sta_offset+1];i++)
				{
					sprintf(pBusSearchEngine->tempString, "%s ", pSoultionHead->pString+pSolutionData[sta_offset+3+i]);
					temLen = strlen(pBusSearchEngine->tempString);
					REALLOC(pBusSearchEngine->output, pBusSearchEngine->outputLen, strLen+temLen);
					MEMCPY(pBusSearchEngine->output+strLen, pBusSearchEngine->tempString, temLen);
					strLen+=temLen;
				}
				sprintf(pBusSearchEngine->tempString, " �� %s(%d)\r\n", pSoultionHead->pString, pSolutionData[sta_offset+2]);
				temLen = strlen(pBusSearchEngine->tempString);
				REALLOC(pBusSearchEngine->output, pBusSearchEngine->outputLen, strLen+temLen);
				MEMCPY(pBusSearchEngine->output+strLen, pBusSearchEngine->tempString, temLen);
				strLen+=temLen;
			}
		}/*************************save bus name***************************************************/	
	}
	sprintf(pBusSearchEngine->tempString, "\r\nȫ��%dվ\r\n\r\n\r\n", pSoultionHead->miniCost);
	temLen = strlen(pBusSearchEngine->tempString);
	REALLOC(pBusSearchEngine->output, pBusSearchEngine->outputLen, strLen+temLen);
	MEMCPY(pBusSearchEngine->output+strLen, pBusSearchEngine->tempString, temLen);
	strLen+=temLen;
	pBusSearchEngine->output[strLen]='\0';
	return (UINT)pBusSearchEngine->output;
}

static void samplesort(UINT16* pData, UINT16* pZero, UINT16* miniCost_S, UINT16* miniCost_D, UINT16 len)
{
	UINT16 i,j, staNo, cost, min;
	UINT16 temp[3];
	
	for(i = 0; i<len-1;i++)
	{
		staNo = pZero[pData[i*3]];
		min = miniCost_S[staNo]+miniCost_D[staNo];
		for(j = i+1; j<len;j++)
		{
			staNo = pZero[pData[j*3]];
			cost = miniCost_S[staNo]+miniCost_D[staNo];
			if(min > cost)
			{
				min = cost;
				temp[0] = pData[j*3];
				temp[1] = pData[j*3+1];
				temp[2] = pData[j*3+2];

				pData[j*3] = pData[i*3];
				pData[j*3+1] = pData[i*3+1];
				pData[j*3+2] = pData[i*3+2];

				pData[i*3] = temp[0];
				pData[i*3+1] = temp[1];
				pData[i*3+2] = temp[2];
			}
		}
	}
}
static UINT SortSolutionStation(struct busSearchEngine* const pBusSearchEngine, UINT16* pSolutionData)//char*
{
	SoultionHead* pSoultionHead=(SoultionHead*)pBusSearchEngine->solutionData;
	UINT16* pQueue = pBusSearchEngine->pStaInQueue;
	UINT16 queue_top = 1;
	UINT16 queue_bot=0;
	UINT8* pQueueTrTimes = (UINT8*)pBusSearchEngine->miniTranTimes;
	
	if(pSolutionData == NULL)
	{
		return (UINT)NULL;
	}

	pQueue[0] = pSoultionHead->station_S_offset;
	pQueueTrTimes[0]=0;
	
	while(queue_top!=queue_bot)
	{
		UINT16 sta_offset, tempOffset, nextOffset, i, l, curTrTime, staNo;
		curTrTime = pQueueTrTimes[queue_bot];
		sta_offset = pQueue[queue_bot++];//�õ�һ��վ
		
		if(curTrTime<pSoultionHead->transfer_times)
		{
			tempOffset = sta_offset;
			do
			{
				i=0;
				do
				{
					nextOffset = pSolutionData[tempOffset+i*3+1];

					for(l=0;l<queue_top;l++)
					{
						if(nextOffset == pQueue[l])
							break;
					}
					if(l == queue_top)
					{
						pQueueTrTimes[queue_top] = curTrTime+1;
						pQueue[queue_top++] = nextOffset;
					}
					i++;
				}while( pSolutionData[tempOffset + i*3 +2] != BLFLAG);

				//�õ����վ��i�����ݴ˳�������
				samplesort(pSolutionData+tempOffset+1, pSolutionData, pBusSearchEngine->miniCost_S, pBusSearchEngine->miniCost_D, i);
				tempOffset+=i*3 +2;
			}while(pSolutionData[tempOffset+1]!=ENDFLAG);

		}
		else
		{
			if(curTrTime == pSoultionHead->transfer_times)
			{
				for(i = 0;i<pSolutionData[sta_offset+1];i++)
				{
					sprintf(pBusSearchEngine->tempString, "%s ", pSoultionHead->pString+pSolutionData[sta_offset+3+i]);
				}
			}
		}
	}
	return (UINT)pBusSearchEngine->output;
}



static UINT SearchLine_WR(struct busSearchEngine* const  pBusSearchEngine, const UINT16 station_S, const UINT16 station_D)
{
	UINT16 busNo, staCnt, busCnt, currentSta, i, k,m,cost, StaS, bNext1=0, bfound=0, tempK, lastSpos;
	int j;
	UINT8 tranferTimes;
	UINT16* pBus_array=NULL, *pSta_array=NULL, *pTempQueue = NULL;
	UINT16	curPos, nextPos, temp, que_bot, que_top;
	UINT8* miniTranTimes, *pStaBeExiest;
	UINT16* pBusNo, *pBusNo2, *pQueue, *pStaNo, *pBusBeS, *pStaInQueue, *miniCost_S, *miniCost_D;
	MainData* pData;
	if(pBusSearchEngine == NULL)
		return (UINT)NULL;
	pData = pBusSearchEngine->pData;
	if(pData != NULL)
		if(station_S >= pData->station_count || station_D >= pData->station_count || station_D == station_S)
			return (UINT)NULL;/*³¬³ö²éÑ¯·¶Î§*/
	if(pBusSearchEngine->firstIn == 1)
	{
		UINT mem_totalsize = 0, fg_BL_size, pStaBeExiest_size, fg_STE_size, fg_ST_size, miniTranTimes_size;
		UINT pBusNo_size, pBusNo2_size, pQueue_size, pStaNo_size, pBusBeS_size;
		UINT pStaInQueue_size, miniCost_S_size, miniCost_D_size, solutionData_size;
		if(pData == NULL)
		{
			MYFREE(pBusSearchEngine->mem_pool);
			pBusSearchEngine->Station_D=0xffff;
			return (UINT)NULL;
		}
		pBusSearchEngine->firstIn = 0;
		mem_totalsize += (fg_BL_size = (pData->bus_count+7)/8*sizeof(UINT8));
		mem_totalsize	 += (pStaBeExiest_size = (pData->station_count+7)/8*sizeof(UINT8));
		mem_totalsize	 += (fg_STE_size = (pData->station_count+7)/8*sizeof(UINT8));
		mem_totalsize	 += (fg_ST_size = (pData->station_count+7)/8*sizeof(UINT8));
		mem_totalsize	 += (miniTranTimes_size = pData->station_count*sizeof(UINT8));
		
		mem_totalsize += ( miniTranTimes_size += ((4-(mem_totalsize%4))%4));
		
		mem_totalsize += (pBusNo_size = pData->station_count*sizeof(UINT16));
		mem_totalsize += (pBusNo2_size = pData->station_count*sizeof(UINT16));
		mem_totalsize += (pQueue_size = pData->station_count*sizeof(UINT16));
		mem_totalsize += (pStaNo_size = pData->station_count*sizeof(UINT16));
		mem_totalsize += (pBusBeS_size = pData->bus_count*sizeof(UINT16));
		
		mem_totalsize += (pStaInQueue_size = pData->station_count*sizeof(UINT16));
		mem_totalsize += (miniCost_S_size = pData->station_count*sizeof(UINT16));
		mem_totalsize += (miniCost_D_size = pData->station_count*sizeof(UINT16));
//		mem_totalsize += (solutionData_size = pBusSearchEngine->solutionDataLen*sizeof(UINT16));
		
		pBusSearchEngine->mem_pool			= (UINT8*)MALLOC(mem_totalsize);
		
		pBusSearchEngine->fg_BL				= pBusSearchEngine->mem_pool;//
		pBusSearchEngine->pStaBeExiest			= pBusSearchEngine->fg_BL			+fg_BL_size;//
		pBusSearchEngine->fg_STE				= pBusSearchEngine->pStaBeExiest	+ pStaBeExiest_size;//
		pBusSearchEngine->fg_ST				= pBusSearchEngine->fg_STE			+ fg_STE_size;//
		pBusSearchEngine->miniTranTimes			= pBusSearchEngine->fg_ST			+ fg_ST_size;//
		
		
		pBusSearchEngine->pBusNo			  	= (UINT16*)(pBusSearchEngine->miniTranTimes							+ miniTranTimes_size);//
		pBusSearchEngine->pBusNo2				= (UINT16*)((UINT8*)pBusSearchEngine->pBusNo						+ pBusNo_size);//
		pBusSearchEngine->pQueue = pBusSearchEngine->StaDataLen	= (UINT16*)((UINT8*)pBusSearchEngine->pBusNo2 	+ pBusNo2_size);//
		pBusSearchEngine->pStaNo 				= (UINT16*)((UINT8*)pBusSearchEngine->pQueue 						+ pQueue_size);//
		pBusSearchEngine->pBusBeS	= 	pBusSearchEngine->pBusQ	= (UINT16*)((UINT8*)pBusSearchEngine->pStaNo 	+ pStaNo_size);//
		
		pBusSearchEngine->pStaInQueue			= (UINT16*)((UINT8*)pBusSearchEngine->pBusBeS 						+ pBusBeS_size);//
		pBusSearchEngine->miniCost_S			= (UINT16*)((UINT8*)pBusSearchEngine->pStaInQueue 					+ pStaInQueue_size);//
		pBusSearchEngine->miniCost_D			= (UINT16*)((UINT8*)pBusSearchEngine->miniCost_S 						+ miniCost_S_size);//
		
//		pBusSearchEngine->solutionData			= (UINT16*)((UINT8*)pBusSearchEngine->miniCost_D 						+ miniCost_D_size);//
		pBusSearchEngine->solutionData			=(UINT16*)MALLOC(pBusSearchEngine->solutionDataLen*sizeof(UINT16));
	}
	else
	{
		if(pData == NULL)
		{
			MYFREE(pBusSearchEngine->mem_pool);
			pBusSearchEngine->Station_D=0xffff;
			return (UINT)NULL;
		}
	}
	{
		miniTranTimes	= pBusSearchEngine->miniTranTimes;
		pStaBeExiest		= pBusSearchEngine->pStaBeExiest;
		pBusNo			= pBusSearchEngine->pBusNo		;
		pBusNo2			= pBusSearchEngine->pBusNo2	;
		pQueue			= pBusSearchEngine->pQueue		;
		pStaNo			= pBusSearchEngine->pStaNo		;
		pBusBeS			= pBusSearchEngine->pBusBeS	;
		pStaInQueue		= pBusSearchEngine->pStaInQueue;
		miniCost_S		= pBusSearchEngine->miniCost_S	;
		miniCost_D		= pBusSearchEngine->miniCost_D	;
	}
	{
		pBusSearchEngine->Station_D = station_D;
		busCnt=pData->pStation[station_D].bus_count;
		pBus_array=pData->pStation[station_D].pBus_array;
		MEMSET(pStaBeExiest, 0, (pData->station_count+7)/8);	
		MEMSET(miniCost_D, 0, pData->station_count*sizeof(UINT16));
		MEMSET(pBusNo2, 0xff, pData->station_count*sizeof(UINT16));
		for(i=0; i<busCnt; i++)
		{
			busNo		= pBus_array[i];
			m = staCnt		= pData->pBus[busNo].station_count;
			pSta_array	= pData->pBus[busNo].pStation_array;
			if(staCnt == 0)
				DEBUG_PRINTF("staCnt == 0  Line:%d\n", __LINE__);
			while(pSta_array[--staCnt]!= station_D) if(staCnt==0) break;
			tempK = staCnt;
			lastSpos = staCnt;
			cost=0;
			while(staCnt--)
			{
				if(pSta_array[staCnt]!=station_D)
					SetFlagTrue(pStaBeExiest, pSta_array[staCnt]);
				else
				{
					cost=0;
					lastSpos = staCnt;//¼ÇÂ¼×îºóµÄÎ»ÖÃ
					continue;
				}
				if(miniCost_D[pSta_array[staCnt]] > ++cost || miniCost_D[pSta_array[staCnt]]==0)
				{
					miniCost_D[pSta_array[staCnt]]	= cost;
					pBusNo2[pSta_array[staCnt]]	= busNo;
				}
			}
			
			if(pData->pBus[busNo].type == 0)
			{
				cost = m-(tempK - lastSpos);
				staCnt = tempK;
				while(++staCnt<m)
				{
					if(pSta_array[staCnt]!=station_D)
						SetFlagTrue(pStaBeExiest, pSta_array[staCnt]);
					else
					{
						DEBUG_PRINTF("Logic ERROR!\nLine:%d\n", __LINE__);
						continue;
					}
					if(miniCost_D[pSta_array[staCnt]] > --cost || miniCost_D[pSta_array[staCnt]]==0)
					{
#ifdef CHECKARRAY
						if(cost == 0)
							DEBUG_PRINTF("COST ERROR == 0\nLine:%d\n", __LINE__);
#endif
						miniCost_D[pSta_array[staCnt]]	= cost;
						pBusNo2[pSta_array[staCnt]]	= busNo;
					}
				}
			}
			else
				if(pData->pBus[busNo].type == 1)
				{
					staCnt = lastSpos;
					cost=0;
					while(++staCnt<m)
					{
						if(pSta_array[staCnt]!=station_D)
							SetFlagTrue(pStaBeExiest, pSta_array[staCnt]);
						else
						{
							cost = 0;
							continue;
						}
						if(miniCost_D[pSta_array[staCnt]] > ++cost || miniCost_D[pSta_array[staCnt]]==0)
						{
							miniCost_D[pSta_array[staCnt]]	= cost;
							pBusNo2[pSta_array[staCnt]]	= busNo;
						}
					}
				}
		}
	}
	

/*1 S0 b1 c1 s1 b2 c2 s2*/
	MEMSET(pBusSearchEngine->Sline, 0x0, MAX_TRANSF_TIMES*3*sizeof(UINT16));
	if(GetFlag(pStaBeExiest,station_S))
	{
		pBusSearchEngine->Sline[0]=0;
		pBusSearchEngine->Sline[1]=station_S;
		pBusSearchEngine->Sline[2]=pBusNo2[station_S];
		pBusSearchEngine->Sline[3]=miniCost_D[station_S];
		pBusSearchEngine->Sline[4]=station_D;
		return (UINT)pBusSearchEngine->Sline;
	}

	{
		MEMSET(miniTranTimes, 0xff, pData->station_count*sizeof(UINT8));
		MEMSET(pBusNo, 0xff,pData->station_count*sizeof(UINT16));
		MEMSET(pBusSearchEngine->Lay_cost_Len, 0x0, MAX_TRANSF_TIMES*sizeof(UINT16));
		
		MEMSET(pBusBeS, 0xff, pData->bus_count*sizeof(UINT16));

		
		miniTranTimes[station_S]=0;

		que_top = 1;
		que_bot = 0;
		pBusSearchEngine->Is_top_bot		= 1;
		pQueue[0]		= station_S;
		
		cost = 0;
		pBusSearchEngine->Lay_cost_Len[0] = 1;
	}
	pBusSearchEngine->expandedNodeCnt=0;
/******************************************************************************************/
	while(que_top>que_bot)
	{
		StaS = pQueue[que_bot++];
		busCnt=pData->pStation[StaS].bus_count;
		pBus_array=pData->pStation[StaS].pBus_array;
		for(i=0; i<busCnt; i++)
		{
			busNo=pBus_array[i];
#ifdef CHECKARRAY
			if(busNo >= pData->bus_count)
			{
				DEBUG_PRINTF("busNo=%d ERROR \nLine:%d\n", busNo,__LINE__);
			}
#endif
			if(busNo==pBusNo[StaS])
				continue;

			if(pData->pBus[busNo].type == 2)
			{
				k=0;while(pData->pBus[busNo].pStation_array[k++]!=StaS);
				if(pBusBeS[busNo]>k)
				{
					staCnt=pData->pBus[busNo].station_count > pBusBeS[busNo] ? pBusBeS[busNo] : pData->pBus[busNo].station_count;
					for(j=k; j<staCnt; j++)
					{
						currentSta = pData->pBus[busNo].pStation_array[j];
	//					if(currentSta == StaS)
	//						continue;
#ifdef CHECKARRAY
						if(currentSta>=pData->station_count)
						{
							DEBUG_PRINTF("currentSta=%d ERROR \nLine:%d\n", currentSta,__LINE__);
						}
#endif
						if(miniTranTimes[currentSta] == 0xff)
						{
							pBusSearchEngine->expandedNodeCnt++;
							
	//						DEBUG_PRINTF("%d\t", expandedNodeCnt);

							miniTranTimes[currentSta]=miniTranTimes[StaS]+1;
							pQueue[que_top++]=currentSta;

							
							pBusNo[currentSta] = busNo;/*¸ÃÕ¾ÊÇÓÉbusNoÀ©Õ¹À´µÄ*/
							pBusSearchEngine->Lay_cost_Len[miniTranTimes[currentSta]]++;
#ifndef BACKSEARCH
							
							if(GetFlag(pStaBeExiest,currentSta))
#else
							if(miniTranTimes[StaS]<MINIBREAKV)
							{
								if(GetFlag(pStaBeExiest,currentSta))
								{
									bfound = 1;
									tranferTimes = miniTranTimes[currentSta];
									bNext1 = 1;
									goto NEXT2;
								}
							}
							else 
							if(currentSta == station_D)
#endif
							{
								bfound = 1;
#ifdef BACKSEARCH
								tranferTimes = miniTranTimes[currentSta]-1;
								goto NEXT1;
#else
								tranferTimes = miniTranTimes[currentSta];
								goto NEXT2;
#endif
								
							}
						}
					}
					pBusBeS[busNo]=k;
				}
			}
			else
			{
				if(pBusBeS[busNo]!=0)
				{
					staCnt=pData->pBus[busNo].station_count;
					for(j=0; j<staCnt; j++)
					{
						currentSta = pData->pBus[busNo].pStation_array[j];
	//					if(currentSta == StaS)
	//						continue;
#ifdef CHECKARRAY
						if(currentSta>=pData->station_count)
						{
							DEBUG_PRINTF("currentSta=%d ERROR \nLine:%d\n", currentSta,__LINE__);
						}
#endif
						if(miniTranTimes[currentSta] == 0xff)
						{
							pBusSearchEngine->expandedNodeCnt++;
							
	//						DEBUG_PRINTF("%d\t", expandedNodeCnt);

							miniTranTimes[currentSta]=miniTranTimes[StaS]+1;
							pQueue[que_top++]=currentSta;

							
							pBusNo[currentSta] = busNo;/*¸ÃÕ¾ÊÇÓÉbusNoÀ©Õ¹À´µÄ*/
							pBusSearchEngine->Lay_cost_Len[miniTranTimes[currentSta]]++;
#ifndef BACKSEARCH
							
							if(GetFlag(pStaBeExiest,currentSta))
#else
							if(miniTranTimes[StaS]<MINIBREAKV)
							{
								if(GetFlag(pStaBeExiest,currentSta))
								{
									bfound = 1;
									tranferTimes = miniTranTimes[currentSta];
									bNext1 = 1;
									goto NEXT2;
								}
							}
							else 
							if(currentSta == station_D)
#endif
							{
								bfound = 1;
#ifdef BACKSEARCH
								tranferTimes = miniTranTimes[currentSta]-1;
								goto NEXT1;
#else
								tranferTimes = miniTranTimes[currentSta];
								goto NEXT2;
#endif
								
							}
						}
					}
					pBusBeS[busNo]=0;
				}
			}
		}
	}
	
	if(bfound == 0)
		return (UINT)NULL;
/******************************************************************************************/
/******************************************************************************************/
/*******************************·´ÏòËÑË÷**********************************************/
#ifdef BACKSEARCH
NEXT1:
	if(miniTranTimes[station_D] != tranferTimes+1)
	{
		DEBUG_PRINTF("FirstSearch can't find station_D!!!\nLine:%d\n", __LINE__);
		return (UINT)pBusSearchEngine->Sline;
	}

	if(!bNext1)
	{
		for(i=0;i<pData->station_count;i++)
			if(miniTranTimes[i]!=0xff)
			{
				miniTranTimes[i]+=0x60;
			}
		miniTranTimes[station_D] = tranferTimes+1;
	 
		que_top = 1;
		que_bot = 0;
		pQueue[0] = station_D;

		
		MEMSET(pBusBeS, 0, pData->bus_count*sizeof(UINT16));
		MEMSET(pBusNo, 0xff, pData->station_count*sizeof(UINT16));
		while(que_top>que_bot)
		{
			StaS = pQueue[que_bot++];
			busCnt=pData->pStation[StaS].bus_count;
			pBus_array=pData->pStation[StaS].pBus_array;
			for(i=0; i<busCnt; i++)
			{
				busNo=pBus_array[i];
				if(busNo==pBusNo[StaS])
					continue;
				if(pData->pBus[busNo].type == 2)
				{
					k=pData->pBus[busNo].station_count;
					while(pData->pBus[busNo].pStation_array[--k]!=StaS);
					if(pBusBeS[busNo]<k)
					{
						//Ò»¶¨Òª·´¹ýÀ´£¬²»È»»á³ö´í£¬Ô­ÒòÔÚÓÚÍ¬Ò»³µ´ÎÀïÍ¬Ò»Õ¾¿ÉÄÜ³öÏÖ¶à´Î
						
						
						for(j=pBusBeS[busNo]; j<k; j++)//·´Ïò
						{
							currentSta = pData->pBus[busNo].pStation_array[j];
							if(currentSta == StaS)
								continue;
							if(miniTranTimes[currentSta]!=0xff && miniTranTimes[currentSta] >= 0x60)
							{//Èç¹ûÊÇÕýÏòËÑË÷µ½µÄ½Úµã
								if(miniTranTimes[currentSta]==miniTranTimes[StaS]-1+0x60)
								{
									pBusSearchEngine->expandedNodeCnt++;
									pQueue[que_top++]=currentSta;
									pBusSearchEngine->Lay_cost_Len[miniTranTimes[currentSta]-0x60]++;
									pBusNo[currentSta] = busNo;//¸ÃÕ¾ÊÇÓÉbusNoÀ©Õ¹À´µÄ
									miniTranTimes[currentSta]=miniTranTimes[StaS]-1;
									
									if(currentSta == station_S)
									{
										if(miniTranTimes[currentSta] != 0)
											DEBUG_PRINTF("ERROR! miniTranTimes[currentSta] != 0\nLine:%d\n", __LINE__);
										goto NEXT2;
									}
								}
								else
									miniTranTimes[currentSta]=0xff;
							}
						}
						pBusBeS[busNo]=k;
					}
				}
				else
				{
					if(pBusBeS[busNo] == 0)
					{
						staCnt=pData->pBus[busNo].station_count;
						for(j = 0; j<staCnt; j++) //·´Ïò
						{//¶ÔÓÚ»½Â·ºÍÍ¬Â·£¬Ã¿¸öÕ¾¶¼¿ÉÒÔµ½´ï
							currentSta = pData->pBus[busNo].pStation_array[j];
							if(currentSta == StaS)
								continue;
		//					if(currentSta == station_S)
		//						DEBUG_PRINTF("Found station_S!\n");
							if(miniTranTimes[currentSta]!=0xff && miniTranTimes[currentSta] >= 0x60)
							{//Èç¹ûÊÇÕýÏòËÑË÷µ½µÄ½Úµã
								if(miniTranTimes[currentSta]==miniTranTimes[StaS]-1+0x60)
								{
									pBusSearchEngine->expandedNodeCnt++;
									pQueue[que_top++]=currentSta;
									pBusSearchEngine->Lay_cost_Len[miniTranTimes[currentSta]-0x60]++;
									pBusNo[currentSta] = busNo;//¸ÃÕ¾ÊÇÓÉbusNoÀ©Õ¹À´µÄ
									miniTranTimes[currentSta]=miniTranTimes[StaS]-1;
									
									if(currentSta == station_S)
									{
										if(miniTranTimes[currentSta] != 0)
											DEBUG_PRINTF("ERROR! miniTranTimes[currentSta] != 0\nLine:%d\n", __LINE__);
										goto NEXT2;
									}
								}
								else
									miniTranTimes[currentSta]=0xff;
							}
						}
						pBusBeS[busNo]=0xff;
					}
				}
			}
		}
		if(miniTranTimes[station_S] != 0)
		{
			DEBUG_PRINTF("BackSearch can't find station_S!!! S=%d %s\tD=%d %s\nLine:%d\n", station_S,pData->pStation[station_S].name, station_D, pData->pStation[station_D].name, __LINE__);
			return (UINT)pBusSearchEngine->Sline;
		}
	}
/******************************************************************************************/
/******************************************************************************************/
	if(bfound == 0)
		DEBUG_PRINTF("Not FOUND!!\n");
#endif
NEXT2:
	{
		MEMSET(pBusNo, 0xff, pData->station_count*sizeof(UINT16));
		MEMSET(miniCost_S, 0xfd, pData->station_count*sizeof(UINT16));
		MEMSET(pStaInQueue, 0xff, pData->station_count*sizeof(UINT16));
		pStaInQueue[station_S] = 0;

		MEMSET(pStaNo, 0xff, pData->station_count*sizeof(UINT16));
#ifdef BACKSEARCH
		if(!bNext1)
			for(i=0;i<pData->station_count;i++)
				if(miniTranTimes[i]!=0xff && miniTranTimes[i]>=0x60)
				{
					miniTranTimes[i]=0xff;
				}
#endif
		que_top = 1;
		que_bot = 0;
		pBusSearchEngine->Is_top_bot		= 1;
		pQueue[0]		= station_S;
		miniCost_S[station_S] = 0;
		miniCost_S[station_D] = 0xffff;
		cost = 0;
		pBusSearchEngine->Lay_cost_Len[0] = 1;
	}
	while(que_top>que_bot)
	{

		StaS = pQueue[que_bot];

		pQueue[que_bot] = pQueue[--que_top];
		pStaInQueue[pQueue[que_bot]] = que_bot;
		
		pTempQueue = pQueue+que_bot-1;
		
		curPos = 1;
		nextPos = 2;
		m = que_top - que_bot;

		while(nextPos<=m)
		{
			if(nextPos+1<=m)
			{
				if(miniCost_S[pTempQueue[nextPos]] <= miniCost_S[pTempQueue[nextPos+1]])
				{
					if(miniCost_S[pTempQueue[curPos]] > miniCost_S[pTempQueue[nextPos]])
					{

						temp = pStaInQueue[pTempQueue[curPos]];
						pStaInQueue[pTempQueue[curPos]] = pStaInQueue[pTempQueue[nextPos]];
						pStaInQueue[pTempQueue[nextPos]] = temp;
						
						temp = pTempQueue[curPos];
						pTempQueue[curPos] = pTempQueue[nextPos];
						pTempQueue[nextPos] = temp;	

						curPos = nextPos;
						nextPos = nextPos*2;
					}
					else
						break;
				}
				else
				{
					if(miniCost_S[pTempQueue[curPos]] > miniCost_S[pTempQueue[nextPos+1]])
					{

						temp = pStaInQueue[pTempQueue[curPos]];
						pStaInQueue[pTempQueue[curPos]] = pStaInQueue[pTempQueue[nextPos+1]];
						pStaInQueue[pTempQueue[nextPos+1]] = temp;
						
						temp = pTempQueue[curPos];
						pTempQueue[curPos] = pTempQueue[nextPos+1];
						pTempQueue[nextPos+1] = temp;	

						curPos = nextPos+1;
						nextPos = (nextPos+1)*2;
					}
					else
						break;

				}
			}
			else
			{
				if(miniCost_S[pTempQueue[curPos]] > miniCost_S[pTempQueue[nextPos]])
				{

					temp = pStaInQueue[pTempQueue[curPos]];
					pStaInQueue[pTempQueue[curPos]] = pStaInQueue[pTempQueue[nextPos]];
					pStaInQueue[pTempQueue[nextPos]] = temp;
					
					temp = pTempQueue[curPos];
					pTempQueue[curPos] = pTempQueue[nextPos];
					pTempQueue[nextPos] = temp;	

					curPos = nextPos;
					nextPos = nextPos*2;
				}
				else
					break;
			}
		}

		if(miniCost_S[StaS]+2 > miniCost_S[station_D] + pBusSearchEngine->exDistance)
			break;
		busCnt=pData->pStation[StaS].bus_count;
		pBus_array=pData->pStation[StaS].pBus_array;
		for(i=0; i<busCnt; i++)
		{
			busNo=pBus_array[i];
			if(pBusNo[StaS]==busNo)
				continue;
			tempK=0;while(pData->pBus[busNo].pStation_array[tempK++]!=StaS);
			
			cost = 0;
			staCnt=pData->pBus[busNo].station_count;

			if(pData->pBus[busNo].type != 0)
			{
				lastSpos = tempK-1;
				for(j=tempK; j<staCnt; j++)
				{
					cost++;
					currentSta = pData->pBus[busNo].pStation_array[j];
#ifdef SAME2SAME
					if(currentSta == StaS)
					{
						cost=0;
						lastSpos = j;
						continue;
					}
#endif
	/*				if(miniCost_S[StaS] + cost + tranferTimes - miniTranTimes[StaS] > miniCost_S[station_D])
						break;*/
					if((miniTranTimes[currentSta] == miniTranTimes[StaS]+1 || GetFlag(pStaBeExiest,currentSta)))
					{
						if(miniCost_S[StaS]+cost<miniCost_S[currentSta])
						{
							miniCost_S[currentSta]	= miniCost_S[StaS]+cost;
							pBusNo[currentSta]	= busNo;
							pStaNo[currentSta]		= StaS;/*¸ÃÕ¾ÊÇÓÉStaSÀ©Õ¹À´µÄ*/

							if(GetFlag(pStaBeExiest,currentSta))
							{//µ±Ç°Õ¾¿ÉÒÔÖ±´ïÄ¿µÄÕ¾
								if(miniCost_S[currentSta]+miniCost_D[currentSta] <= miniCost_S[station_D])
								{
									miniCost_S[station_D]	= miniCost_S[currentSta]+miniCost_D[currentSta];
									miniTranTimes[currentSta] = tranferTimes;
									pStaNo[station_D]	= currentSta;
									pBusNo[station_D]	= pBusNo2[currentSta];
								}
							}
							else
								if(miniTranTimes[currentSta]< tranferTimes)
								{
									if(pStaInQueue[currentSta] == 0xffff)
									{//²»ÔÚ¶ÓÁÐÖÐ
										pStaInQueue[currentSta] = que_top;
										pQueue[que_top++] = currentSta;
									}

									curPos = pStaInQueue[currentSta] - que_bot+1;
									nextPos = curPos/2;
									pTempQueue = pQueue+que_bot-1;

									while(nextPos>0)
									{
										
										if(miniCost_S[pTempQueue[curPos]] < miniCost_S[pTempQueue[nextPos]])
										{
											temp = pStaInQueue[pTempQueue[curPos]];
											pStaInQueue[pTempQueue[curPos]] = pStaInQueue[pTempQueue[nextPos]];
											pStaInQueue[pTempQueue[nextPos]] = temp;
											
											temp = pTempQueue[curPos];
											pTempQueue[curPos] = pTempQueue[nextPos];
											pTempQueue[nextPos] = temp;

											curPos = nextPos;
											nextPos = nextPos/2;
										}
										else
											break;
									}
								}
						}
					}
				}

				if(pData->pBus[busNo].type == 1)
				{					
					cost = 0;
					for(j=lastSpos-1; j>=0; j--)
					{
						cost++;
						currentSta = pData->pBus[busNo].pStation_array[j];
#ifdef SAME2SAME
						if(currentSta == StaS)
						{
							cost=0;
							continue;
						}
#endif
		/*				if(miniCost_S[StaS] + cost + tranferTimes - miniTranTimes[StaS] > miniCost_S[station_D])
							break;*/
						if((miniTranTimes[currentSta] == miniTranTimes[StaS]+1 || GetFlag(pStaBeExiest,currentSta)))
						{
							if(miniCost_S[StaS]+cost<miniCost_S[currentSta])
							{
								miniCost_S[currentSta]	= miniCost_S[StaS]+cost;
								pBusNo[currentSta]	= busNo;
								pStaNo[currentSta]		= StaS;/*¸ÃÕ¾ÊÇÓÉStaSÀ©Õ¹À´µÄ*/

								if(GetFlag(pStaBeExiest,currentSta))
								{//µ±Ç°Õ¾¿ÉÒÔÖ±´ïÄ¿µÄÕ¾
									if(miniCost_S[currentSta]+miniCost_D[currentSta] <= miniCost_S[station_D])
									{
										miniCost_S[station_D]	= miniCost_S[currentSta]+miniCost_D[currentSta];
										miniTranTimes[currentSta] = tranferTimes;
										pStaNo[station_D]	= currentSta;
										pBusNo[station_D]	= pBusNo2[currentSta];
									}
								}
								else
									if(miniTranTimes[currentSta]< tranferTimes)
									{
										if(pStaInQueue[currentSta] == 0xffff)
										{//²»ÔÚ¶ÓÁÐÖÐ
											pStaInQueue[currentSta] = que_top;
											pQueue[que_top++] = currentSta;
										}

										curPos = pStaInQueue[currentSta] - que_bot+1;
										nextPos = curPos/2;
										pTempQueue = pQueue+que_bot-1;

										while(nextPos>0)
										{
											
											if(miniCost_S[pTempQueue[curPos]] < miniCost_S[pTempQueue[nextPos]])
											{
												temp = pStaInQueue[pTempQueue[curPos]];
												pStaInQueue[pTempQueue[curPos]] = pStaInQueue[pTempQueue[nextPos]];
												pStaInQueue[pTempQueue[nextPos]] = temp;
												
												temp = pTempQueue[curPos];
												pTempQueue[curPos] = pTempQueue[nextPos];
												pTempQueue[nextPos] = temp;

												curPos = nextPos;
												nextPos = nextPos/2;
											}
											else
												break;
										}

									}
							}
						}
					}
				}
			}
			else// if(pData->pBus[busNo].type == 0)
			{
				for(j = tempK%staCnt; j!=tempK-1; j=(j+1)%staCnt)
				{
					cost++;
					currentSta = pData->pBus[busNo].pStation_array[j];
#ifdef SAME2SAME
					if(currentSta == StaS)
					{
						cost=0;
						continue;
					}
#endif
	/*				if(miniCost_S[StaS] + cost + tranferTimes - miniTranTimes[StaS] > miniCost_S[station_D])
						break;*/
					if((miniTranTimes[currentSta] == miniTranTimes[StaS]+1 || GetFlag(pStaBeExiest,currentSta)))
					{
						if(miniCost_S[StaS]+cost<miniCost_S[currentSta])
						{
							miniCost_S[currentSta]	= miniCost_S[StaS]+cost;
							pBusNo[currentSta]	= busNo;
							pStaNo[currentSta]		= StaS;/*¸ÃÕ¾ÊÇÓÉStaSÀ©Õ¹À´µÄ*/
							if(currentSta == station_D)
								DEBUG_PRINTF("ERROR\nLine:%d\n", __LINE__);
							if(GetFlag(pStaBeExiest,currentSta))
							{//µ±Ç°Õ¾¿ÉÒÔÖ±´ïÄ¿µÄÕ¾
								if(miniCost_S[currentSta]+miniCost_D[currentSta] <= miniCost_S[station_D])
								{
									miniCost_S[station_D]	= miniCost_S[currentSta]+miniCost_D[currentSta];
									miniTranTimes[currentSta] = tranferTimes;
									pStaNo[station_D]	= currentSta;
									pBusNo[station_D]	= pBusNo2[currentSta];
								}
							}
							else
								if(miniTranTimes[currentSta]< tranferTimes)
								{
									if(pStaInQueue[currentSta] == 0xffff)
									{//²»ÔÚ¶ÓÁÐÖÐ
										pStaInQueue[currentSta] = que_top;
										pQueue[que_top++] = currentSta;
									}
									curPos = pStaInQueue[currentSta] - que_bot+1;
									nextPos = curPos/2;
									pTempQueue = pQueue+que_bot-1;

									while(nextPos>0)
									{
										
										if(miniCost_S[pTempQueue[curPos]] < miniCost_S[pTempQueue[nextPos]])
										{
											temp = pStaInQueue[pTempQueue[curPos]];
											pStaInQueue[pTempQueue[curPos]] = pStaInQueue[pTempQueue[nextPos]];
											pStaInQueue[pTempQueue[nextPos]] = temp;
											
											temp = pTempQueue[curPos];
											pTempQueue[curPos] = pTempQueue[nextPos];
											pTempQueue[nextPos] = temp;

											curPos = nextPos;
											nextPos = nextPos/2;
										}
										else
											break;
									}
								}
						}
					}
				}
			}
		}
	}
/******************************************************************************************/
	/*1 S0 b1 c1 s1 b2 c2 s2*/
	pBusSearchEngine->Sline[0]=tranferTimes;
	pBusSearchEngine->Sline[1]=station_S;
	
	currentSta = station_D;
	tranferTimes+=1;
	if(tranferTimes>1)
	{		
		BuildSolutionStream(pBusSearchEngine, station_S, 0, 0xffff, 0, (UINT8)(tranferTimes-1), miniCost_S[station_D], station_D);
	}
	
	while(tranferTimes)
	{
		pBusSearchEngine->Sline[(tranferTimes-1)*3+2]	= pBusNo[currentSta];
		pBusSearchEngine->Sline[(tranferTimes-1)*3+2+1]	= miniCost_S[currentSta];
		pBusSearchEngine->Sline[(tranferTimes-1)*3+2+2]	= currentSta;
		currentSta = pStaNo[currentSta];
		tranferTimes--;
	};
	
	return (UINT)pBusSearchEngine->Sline;
}


static UINT SlineToString(struct busSearchEngine* const pBusSearchEngine, const UINT16* Sline)
{
	UINT16 i;
	size_t offset=0;
	MEMSET(pBusSearchEngine->tempString, 0 , 1024);
	MEMCPY(pBusSearchEngine->tempString, "�� ", 3);offset+=3;
	MEMCPY(pBusSearchEngine->tempString+offset, pBusSearchEngine->pData->pStation[Sline[1]].name, STRLEN(pBusSearchEngine->pData->pStation[Sline[1]].name));offset+=STRLEN(pBusSearchEngine->pData->pStation[Sline[1]].name);
	MEMCPY(pBusSearchEngine->tempString+offset, " ���� �� ", 8); offset+=8;
	for(i=0;i<Sline[0];i++)
	{
		MEMCPY(pBusSearchEngine->tempString+offset, pBusSearchEngine->pData->pBus[Sline[2+i*3]].name, STRLEN(pBusSearchEngine->pData->pBus[Sline[2+i*3]].name));offset+=STRLEN(pBusSearchEngine->pData->pBus[Sline[2+i*3]].name);
		MEMCPY(pBusSearchEngine->tempString+offset, "  �� ",4);offset+=4;
		MEMCPY(pBusSearchEngine->tempString+offset,pBusSearchEngine->pData->pStation[Sline[2+i*3+2]].name, STRLEN(pBusSearchEngine->pData->pStation[Sline[2+i*3+2]].name));offset+=STRLEN(pBusSearchEngine->pData->pStation[Sline[2+i*3+2]].name);
		MEMCPY(pBusSearchEngine->tempString+offset, "  ת�� ",6);offset+=6;
	}
	if(Sline[0] > 0)
	{
		MEMCPY(pBusSearchEngine->tempString+offset, pBusSearchEngine->pData->pBus[Sline[2+i*3]].name, STRLEN(pBusSearchEngine->pData->pBus[Sline[2+i*3]].name));offset+=STRLEN(pBusSearchEngine->pData->pBus[Sline[2+i*3]].name);
		MEMCPY(pBusSearchEngine->tempString+offset," �� ",4); offset+=4;}
	else
	{
		MEMCPY(pBusSearchEngine->tempString+offset, pBusSearchEngine->pData->pBus[Sline[2+i*3]].name, STRLEN(pBusSearchEngine->pData->pBus[Sline[2+i*3]].name));offset+=STRLEN(pBusSearchEngine->pData->pBus[Sline[2+i*3]].name);
		MEMCPY(pBusSearchEngine->tempString+offset," ֱ�� ",6); offset+=6;}
	MEMCPY(pBusSearchEngine->tempString+offset,pBusSearchEngine->pData->pStation[Sline[2+i*3+2]].name, STRLEN(pBusSearchEngine->pData->pStation[Sline[2+i*3+2]].name));offset+=STRLEN(pBusSearchEngine->pData->pStation[Sline[2+i*3+2]].name);
	pBusSearchEngine->tempString[offset]=0;
	return (UINT)pBusSearchEngine->tempString;
}

static void DBusSearchEngine(struct busSearchEngine** ppBusSearchEngine)
{
	if(ppBusSearchEngine == NULL)
		return;
	if(*ppBusSearchEngine == NULL)
		return;
	MYFREE((*ppBusSearchEngine)->mem_pool);
	MYFREE((*ppBusSearchEngine)->pData);
	MYFREE((*ppBusSearchEngine)->tempArray);
	MYFREE((*ppBusSearchEngine)->output);
	MYFREE((*ppBusSearchEngine)->solutionData);
	MYFREE(*ppBusSearchEngine);
}

UINT CBusSearchEngine(UINT8* stream)
{
	struct busSearchEngine* pBusSearchEngine = (struct busSearchEngine*)MALLOC(sizeof(struct busSearchEngine));
	if(pBusSearchEngine == NULL)
		return (UINT)NULL;
	MEMSET(pBusSearchEngine, 0, sizeof(struct busSearchEngine));
	pBusSearchEngine->miniCost_S=NULL;
	pBusSearchEngine->miniCost_D=NULL;
	pBusSearchEngine->StaDataLen=NULL;
	pBusSearchEngine->solutionData=NULL;
	pBusSearchEngine->pBusQ = NULL;
	pBusSearchEngine->miniTranTimes=NULL;
	pBusSearchEngine->fg_BL=NULL;
	pBusSearchEngine->fg_ST=NULL;
	pBusSearchEngine->fg_STE=NULL;
	pBusSearchEngine->fg_CirLine=NULL;
	pBusSearchEngine->DataSize=0;
	pBusSearchEngine->exCnt=0;
	pBusSearchEngine->solutionDataLen=1024;
	pBusSearchEngine->DataSize3 = 0;
	pBusSearchEngine->firstIn=1;
	pBusSearchEngine->Station_D = 0xffff;
	pBusSearchEngine->pData = loadData(stream);

	pBusSearchEngine->MaxDirOffset= 1024;
	pBusSearchEngine->tempArray=NULL;

	pBusSearchEngine->outputLen = 512;
	pBusSearchEngine->output = NULL;

	pBusSearchEngine->exDistance = 0;
	pBusSearchEngine->loadFromFile = 0;
	if(pBusSearchEngine->pData == NULL)
	{
		FREE(pBusSearchEngine);
		return (UINT)NULL;
	}
	pBusSearchEngine->SearchDAG_depth		=	SearchDAG_depth;
	pBusSearchEngine->SearchDAG_depth4Bulid	=	SearchDAG_depth4Bulid;
	pBusSearchEngine->CompleteSolutionStream	=	CompleteSolutionStream;
	pBusSearchEngine->ReviewSolutionStream		=	ReviewSolutionStream;
	pBusSearchEngine->BuildSolutionStream		=	BuildSolutionStream;
	pBusSearchEngine->SearchLine_WR			=	SearchLine_WR;
	pBusSearchEngine->SlineToString			=	SlineToString;
	pBusSearchEngine->DBusSearchEngine		=	DBusSearchEngine;
	return (UINT)pBusSearchEngine;
}

UINT Engine_LoadData(char fileName[])
{
	UINT32 length;
	struct busSearchEngine* pBusSearchEngine = (struct busSearchEngine*)CBusSearchEngine((UINT8*)MyReadFile(fileName, &length));
	pBusSearchEngine->loadFromFile = 1;
	return (UINT)pBusSearchEngine;
}

UINT Engine_SearchLine(UINT engineHandle, UINT16 Sta_S, UINT16 Sta_D)
{
	struct busSearchEngine* pBusSearchEngine = (struct busSearchEngine*)engineHandle;
	UINT16* ps = (UINT16*)pBusSearchEngine->SearchLine_WR(pBusSearchEngine, Sta_S, Sta_D);
	if(ps!=NULL)
	{
		if(ps[0] > 0)
			return pBusSearchEngine->ReviewSolutionStream(pBusSearchEngine, pBusSearchEngine->solutionData);
		else
			return pBusSearchEngine->SlineToString(pBusSearchEngine,  ps);
	}
	else
		return (UINT)NULL;
}

UINT Engine_SearchLine_org(UINT engineHandle, UINT16 Sta_S, UINT16 Sta_D)
{
	struct busSearchEngine* pBusSearchEngine = (struct busSearchEngine*)engineHandle;
	UINT16* ps;
	if(engineHandle == 0)
		return 0;
	ps = (UINT16*)pBusSearchEngine->SearchLine_WR(pBusSearchEngine, Sta_S, Sta_D);
	return (UINT)pBusSearchEngine->solutionData;
}

UINT Engine_SetExDistance(UINT engineHandle, UINT16 exDistance)
{
	struct busSearchEngine* pBusSearchEngine = (struct busSearchEngine*)engineHandle;
	if(engineHandle == 0)
		return 0xffff;
	pBusSearchEngine->exDistance = exDistance;
	return exDistance;
}

UINT Engine_GetCityName(UINT engineHandle)
{
	struct busSearchEngine* pBusSearchEngine = (struct busSearchEngine*)engineHandle;
	if(engineHandle == 0)
		return 0;
	if(pBusSearchEngine->pData == NULL)
		return 0;
	return (UINT)pBusSearchEngine->pData->city_name;
}

UINT Engine_GetExDistance(UINT engineHandle)
{
	struct busSearchEngine* pBusSearchEngine = (struct busSearchEngine*)engineHandle;
	if(engineHandle == 0)
		return 0xffff;
	return pBusSearchEngine->exDistance;
}

UINT Engine_Destroy(UINT engineHandle)
{
	struct busSearchEngine* pBusSearchEngine = (struct busSearchEngine*)engineHandle;
	if(pBusSearchEngine == NULL)
		return 1;
	MYFREE(pBusSearchEngine->mem_pool);
	if(pBusSearchEngine->loadFromFile)
		MYFREE(pBusSearchEngine->pData);
	MYFREE(pBusSearchEngine->tempArray);
	MYFREE(pBusSearchEngine->output);
	MYFREE(pBusSearchEngine);
	return 0;
}

UINT Engine_GetStationCount(UINT engineHandle)
{
	struct busSearchEngine* pBusSearchEngine = (struct busSearchEngine*)engineHandle;
	if(pBusSearchEngine == NULL)
		return 0;
	return (UINT)pBusSearchEngine->pData->station_count;
}

UINT Engine_GetBuslineCount(UINT engineHandle)
{
	struct busSearchEngine* pBusSearchEngine = (struct busSearchEngine*)engineHandle;
	if(pBusSearchEngine == NULL)
		return 0;
	return (UINT)pBusSearchEngine->pData->bus_count;
}

UINT Engine_GetStationName(UINT engineHandle, UINT16 stationIndex)
{
	struct busSearchEngine* pBusSearchEngine = (struct busSearchEngine*)engineHandle;
	if(pBusSearchEngine == NULL)
		return (UINT)NULL;
	if(stationIndex >= pBusSearchEngine->pData->station_count)
		return (UINT)NULL;
	return (UINT)pBusSearchEngine->pData->pStation[stationIndex].name;
}

UINT Engine_GetBuslineName(UINT engineHandle, UINT16 buslineIndex)
{
	struct busSearchEngine* pBusSearchEngine = (struct busSearchEngine*)engineHandle;
	if(pBusSearchEngine == NULL)
		return (UINT)NULL;
	if(pBusSearchEngine->pData == NULL)
		return (UINT)NULL;
	if(buslineIndex >= pBusSearchEngine->pData->bus_count)
		return (UINT)NULL;
	return (UINT)pBusSearchEngine->pData->pBus[buslineIndex].name;
}

UINT Engine_GetStaCntInBusline(UINT engineHandle, UINT16 buslineIndex)
{
	struct busSearchEngine* pBusSearchEngine = (struct busSearchEngine*)engineHandle;
	if(pBusSearchEngine == NULL)
		return 0xffff;
	if(buslineIndex >= pBusSearchEngine->pData->bus_count)
		return 0xffff;
	return (UINT)pBusSearchEngine->pData->pBus[buslineIndex].station_count;
}

UINT Engine_GetBusCntInStation(UINT engineHandle, UINT16 stationIndex)
{
	struct busSearchEngine* pBusSearchEngine = (struct busSearchEngine*)engineHandle;
	if(pBusSearchEngine == NULL)
		return 0xffff;
	if(pBusSearchEngine->pData == NULL)
		return 0xffff;
	if(stationIndex >= pBusSearchEngine->pData->station_count)
		return 0xffff;
	return (UINT)pBusSearchEngine->pData->pStation[stationIndex].bus_count;
}

UINT Engine_GetStaInBusline(UINT engineHandle, UINT16 buslineIndex, UINT16 staInbusNo)
{
	struct busSearchEngine* pBusSearchEngine = (struct busSearchEngine*)engineHandle;
	if(pBusSearchEngine == NULL)
		return 0xffff;
	if(pBusSearchEngine->pData == NULL)
		return 0xffff;
	if(buslineIndex >= pBusSearchEngine->pData->bus_count)
		return 0xffff;
	if(staInbusNo >= pBusSearchEngine->pData->pBus[buslineIndex].station_count)
		return 0xffff;
	return (UINT)pBusSearchEngine->pData->pBus[buslineIndex].pStation_array[staInbusNo];
}

UINT Engine_GetBusInStation(UINT engineHandle, UINT16 stationIndex, UINT16 busInstaNo)
{
	struct busSearchEngine* pBusSearchEngine = (struct busSearchEngine*)engineHandle;
	if(pBusSearchEngine == NULL)
		return 0xffff;
	if(pBusSearchEngine->pData == NULL)
		return 0xffff;
	if(stationIndex >= pBusSearchEngine->pData->station_count)
		return 0xffff;
	if(busInstaNo >= pBusSearchEngine->pData->pStation[stationIndex].bus_count)
		return 0xffff;
	return (UINT)pBusSearchEngine->pData->pStation[stationIndex].pBus_array[busInstaNo];
}

UINT Engine_GetBuslineDesc(UINT engineHandle, UINT16 buslineIndex)
{
	struct busSearchEngine* pBusSearchEngine = (struct busSearchEngine*)engineHandle;
	if(pBusSearchEngine == NULL)
		return (UINT)NULL;
	if(pBusSearchEngine->pData == NULL)
		return (UINT)NULL;
	if(buslineIndex >= pBusSearchEngine->pData->bus_count)
		return (UINT)NULL;
	return (UINT)pBusSearchEngine->pData->pBus[buslineIndex].description;
}
