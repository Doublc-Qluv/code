#include "bus_engine.h"
#include <stdio.h>
#include <pthread.h>
#include<sys/types.h>
#include<dirent.h>
#include<errno.h>

#define THREADS 8
 pthread_mutex_t mutex[THREADS];
void oneThread(void*  engine_handle)
{
	UINT stacnt, i, j;
	char path[1024];
	int thred_id = *((UINT*)engine_handle+1);
	int start, end;
	stacnt = Engine_GetStationCount(*(UINT*)engine_handle);
	Engine_SetExDistance(*(UINT*)engine_handle, 99);
	start = (stacnt/THREADS)*thred_id;
	if(thred_id < THREADS-1)
		end = start+(stacnt/THREADS);
	else
		end = stacnt;
	printf("thread:%d start: %d	end: %d\n", thred_id, start, end);
	pthread_mutex_lock(&mutex[thred_id]);
	for(i = start; i<end ; i++)
	{
		sprintf(path, "%s.txt", Engine_GetStationName(*(UINT*)engine_handle, i));
		
		FILE* pf = fopen(path, "w");
		if(pf == NULL)
		{
			printf("create %s fault!\n", path);
			return;
		}
		for(j = 0; j<stacnt ; j+=1)
		{
			UINT16* ret;
			if( i  == j)
				continue;
	//		ret = (UINT16*)Engine_SearchLine_org(*(UINT*)engine_handle, i,j);
	//		fwrite(ret, 1, (*ret), pf);
			fprintf(pf, "%s", (char*)Engine_SearchLine(*(UINT*)engine_handle, i,j));
		}
		fclose(pf);
		printf("thread:%d %d	\n", thred_id, i);
	//	sleep(1);
	}
	pthread_mutex_unlock(&mutex[thred_id]);
}

int main()
{
	UINT engine_handle[THREADS*2], i, j, stacnt;
	UINT32 flength;
//	int dirExits = dir_exits("output");
	pthread_t thread_id[THREADS];
	UINT8* stream = (UINT8*)MyReadFile("busLine.dat", &flength);
//	if(dirExits == 0)
	{
//		createdir("output");
	}
	if(stream == NULL)
	{
		printf("stream == NULL");
		return -1;
	}
	
	for( i =0; i<THREADS; i++)
	{
		engine_handle[i*2] = CBusSearchEngine(stream);
		engine_handle[i*2+1] = i;
	}
	

	for( i =0; i<THREADS; i++)
	{
		pthread_mutex_lock(&mutex[i]);
		pthread_create(&thread_id[i], NULL, (void*)&oneThread, &engine_handle[i*2]);
	}
	for( i =0; i<THREADS; i++)
	{
		pthread_mutex_unlock(&mutex[i]);
	}
	for( i =0; i<THREADS; i++)
	{
		pthread_join(thread_id[i], NULL);
	}
	
	printf("\nfinished\n");
	for( i =0; i<THREADS; i++)
		Engine_Destroy(engine_handle[i*2]);
	free(stream);
	return 0;
}

