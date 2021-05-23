mtype = {a,b,Err};

chan AtoB = [1] of {mtype,byte};
chan BtoA = [1] of {mtype,byte};

proctype A(chan  InCh,OutCh)
{
	S5:
		if
		::OutCh!a(0) 
		::OutCh!Err(0)
		fi;
	S4:	
		if
		::InCh?b(0) -> goto S1
		::InCh?b(1) -> goto S1
		::InCh?Err -> goto S5
		fi;
	S1:	
		if
		::OutCh!a(1)
		::OutCh!Err(0)
		fi;
	S2:	
		if
		::InCh?b(0) -> goto S3
		::InCh?b(1) -> goto S1
		::InCh?Err -> goto S5
		fi;
	S3:	
		if
		::OutCh!a(1)
		::OutCh!Err(0)
		fi;
		goto S2;
}
	
proctype B(chan InCh,OutCh)
{
	S4:
		 if 
		::InCh?a(0) -> goto S1
		::InCh?a(1) -> goto S1
		::InCh?Err(0) -> goto S5
		fi;
	S1:
		if
		::OutCh!b(1)
		::OutCh!Err(0)
		fi;
	S2:	
		if
		::InCh?a(0) -> goto S3
		::InCh?a(1) -> goto S1
		::InCh?Err(0) -> goto S5
		fi;
	S3:	
		if
		::OutCh!b(1)
		::OutCh!Err(0)
		fi;
		goto S2;
	S5:
		if
		::OutCh!b(0)
		::OutCh!Err(0)
		fi;
		goto S4;
}
	
	init
	{
		atomic
		{	
			run A(BtoA,AtoB);
			run B(AtoB,BtoA);
		}
	}
