#ifndef __BASIC_TYPES_H__
#define __BASIC_TYPES_H__
#include <string.h>
#include <malloc.h>

typedef char			INT8;
typedef unsigned char	UINT8;

typedef short			INT16;
typedef unsigned short	UINT16;

typedef unsigned long UINT;
typedef long			INT32;
typedef unsigned long	UINT32;

//we recommand not using BOOL as return value, just use RET_CODE
typedef int				BOOL;
#define	FALSE			0
#define	TRUE			(!FALSE)


#define NULL 			((void *)0)

#define MEMSET(dest, viou, src)	memset(dest, viou, src)
#define MALLOC(size)				malloc(size)
#define FREE(ptr)					free(ptr)
#define MEMCPY(dest, len, src)		memcpy(dest, len, src)
#define STRLEN(str)				strlen(str)
//use void, NO VOID exist

//typedef UINT32			HANDLE;
//#define	INVALID_HANDLE	((HANDLE)0xFFFFFFFF)


#endif	//__BASIC_TYPES_H__
