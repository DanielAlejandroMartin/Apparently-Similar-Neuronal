!This is the Fortran 90 code the KC model local implementation in
!"Apparently similar neuronal dynamics may lead to different collective repertoire"
! main program chooses a series of sigma_p values and calls "ConstantStep" Subroutine
! "ConstantStep" runs "stepnum" steps for each value of sigma_p, calling "Step" subroutine each time
! "Step" subroutine updates the state of each neuron simultaneously.
! The program returns f_s and AC(1) for each value of sigma_p
!

!compile using gfortran -O3 KC_l.f90
!run with ./a.out on a terminal






module variables
!Network parameters 
	integer,parameter::  N= 20000 !=Number of Neurons= Network size
	integer,parameter:: Avg_degree=10 !=<k> here in degree is equal to out degree
	integer,parameter:: Nbonds=N*Avg_degree/2
!Time Parameters
	integer,parameter:: stepnum=50000    
	integer,parameter::     MeassTime=0.9*stepnum
	integer,parameter::   transient=0.1*stepnum
!Model Parameters
	real(8),parameter:: r1= 0.001  !Spontaneous activation 
	integer,parameter:: nrefract=3 !nuumber of times at the refractary step n=2+nrefract
	integer,parameter:: nstates=nrefract+2
	real(8),parameter:: lambda=12.5
!Threshold Variables
	real(8)::  sigma_p  ! Threshold T
	real(8),parameter::  Delta_sigma=0.05 ! Threshold Change
	real(8),parameter:: sigma_0=0.45 !lowest value of sigma_p
	real(8),parameter:: sigma_F=2.05 !highest value of sigma_p
	real(8):: Prob
!Neuron States and  Neighbor lists
	integer S(1:N) !Neuron State
	integer S_prev(1:N) !Previous Neuron State
	integer,parameter:: x1=5*Avg_degree
	integer,dimension(N):: MyNeighbors=0 ! MyNeighbors(i) = Ammount of neighbors of i
	integer,dimension(N,x1):: NeighborMat=0 ! NeighborMat(i,k)= identity of the k-tjh neighbor of i
	real(8),dimension(N,x1):: Wij=0 ! Wij(i,k)= weight of the k-tjh connetcion of i, i.e., the conection with  NeighborMat(i,k)
	real(8),dimension(N,x1):: sigmaWij=0 !Auxilliary matrix = sigma_P W_ij
	real(8)::weight    
!OBSERVABLES		
	integer:: activity,prev_activity
	real(8):: AVGact,AVGact2,AvgActPrev
	real(8):: f_s, varf_s,AC1  !fraction of actives, variance of activity and first autocorrelation coefficient
!AUXILIAR VARIABLES
	integer it !iteration step
	integer i,j, jj,k
	real(8) p !for random numbers
end module



program KC_l
use variables
implicit none   

!Load connection matrix and generate weights
open(99,file= "MyMatrix.txt",status="old",action="read")
do k=1,Nbonds
read(99,*) i,j
p=rand(); weight=p

MyNeighbors(i)=MyNeighbors(i)+1
NeighborMat(i,MyNeighbors(i))=j
Wij(i,MyNeighbors(i))=weight
				
MyNeighbors(j)=MyNeighbors(j)+1
NeighborMat(j,MyNeighbors(j))=i
Wij(j,MyNeighbors(j))=weight				
enddo	    
close(99)


		

 do i=1,N; p=rand();  S(i)= int(p*3)
enddo
            
 ! RUN
open(101,file= "Results.txt",status="unknown")           
            
do sigma_p=sigma_0,sigma_F,delta_sigma 

!notice the difference with the original model here:
sigmaWij=Wij*sigma_p ! sigmaWij = sigma_p * WiJ
call ConstantStep
enddo
close(101)
! RUN Backwards 
open(101,file= "BackResults.txt",status="unknown")
do sigma_p=sigma_F,sigma_0,-delta_sigma 
sigmaWij=Wij*sigma_p ! sigmaWij = sigma_p * WiJ
call ConstantStep
enddo
close(101)


end program

!------------------------------------------------

subroutine ConstantStep
use variables;
implicit none
do it=1,transient;call step;enddo
avgact=0;avgact2=0;AvgActPrev=0
do it=1,MeassTime;prev_activity=activity;call step
avgact=avgact+activity;
avgact2=avgact2+activity**2;
AvgActPrev=AvgActPrev+activity*prev_activity
enddo
avgact=avgact/real(measstime);
avgact2=avgact2/real(measstime)
AvgActPrev=AvgActPrev/real(measstime)


f_s= avgact/real(N)
varf_s= real(avgact2-avgact**2)/real(N)**2
AC1= real((AvgActPrev-avgact**2)/(avgact2-avgact**2))

write(101,*) real(sigma_p ),f_s, varf_s, AC1
write(*,*) real(sigma_p ),f_s, varf_s, AC1
end subroutine

!------------------------------------------------


subroutine step
use variables;
implicit none
integer Normalization

S_prev=S
S=0
!Activity=0
do i=1,N

!Previously active -> Refractory P=1
if (S_prev(i)>1) then
S(i)=S_prev(i)+1;
if (S(i)==nstates)  S(i)=0;
endif 

if (S_prev(i).eq.0)then !Previously Quiescent- > Excited P=r1
!	s(i)=0
	p=rand()
	if (p<r1)then
		S(i)=1;
	endif
endif

if (S_prev(i)==1) then
! New Part
        Normalization=0
        do k=1,MyNeighbors(i)					
            j=NeighborMat(i,k)					
            if (S_prev(j)==0) then
            Normalization=Normalization+1					
            endif								
        end do      
! End Normalization calculation
	do k=1,MyNeighbors(i)	
		j=NeighborMat(i,k)	
		if (S_prev(j)==0) then	
				p=rand()
				!Notice the difference Here
			if (p<sigmaWij(i,k)*2/real(Normalization)) then		
				S(j)=1
			endif	
		endif	
	end do     
S(i)=2
end if
end do !N

Activity=0
do i=1,N        
if (S(i)==1) activity=activity+1
end do !N
end subroutine



    
                
