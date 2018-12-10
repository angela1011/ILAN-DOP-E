        program is2timod
c---------------------------------------------------------------------c
c                                                                     c
c      COMPUTER PROGRAMS IN SEISMOLOGY                                c
c      VOLUME V                                                       c
c                                                                     c
c      PROGRAM: TI2ISMOD                                              c
c                                                                     c
c      COPYRIGHT 2002                                                 c
c      R. B. Herrmann                                                 c
c      Department of Earth and Atmospheric Sciences                   c
c      Saint Louis University                                         c
c      221 North Grand Boulevard                                      c
c      St. Louis, Missouri 63013                                      c
c      U. S. A.                                                       c
c                                                                     c
c---------------------------------------------------------------------c
c       CHANGES                                                                
c       05 MAY 2002 - created this program
c-----
c       SYNOPSIS - This program reads a MODEL96 c
c                     file from the standard input
c           The model is either a 1-D CONSTANT LAYER VELOCITY MODEL that
c           is either Isotropic of Transverse Isotropic.
c           The input is from the standard input
c
c           The output is the Transverse Isotropic model file
c           of Dahlen and Tromp (1998)
c-----
        implicit none
        integer LIN, LOT, LER
        parameter (LIN=5,LOT=6,LER=0)

        integer NL
        parameter (NL=200)
        common/timodel/d(NL),TA(NL),TC(NL),TL(NL),TN(NL),TF(NL),
     1      TRho(NL),
     2      qa(NL),qb(NL),etap(NL),etas(NL), 
     3      frefp(NL), frefs(NL)
        real d,TA,TC,TN,TL,TF,TRho,qa,qb,etap,etas,frefp,frefs
        common/depref/refdep
        real refdep

        integer lgstr
        integer iunit,iiso,iflsph,idimen,icnvel
        integer ierr            

        common/modlly/mmax
        integer mmax
        character title*80     
        character mname*80

        integer lt

c-----
c       read in the earth model
c-----
        
        title = ' '
        mname = 'STDIN'
        call getmod(1,mname,mmax,title,iunit,iiso,iflsph,
     1          idimen,icnvel,ierr,.false.)
        lt = lgstr(title)
c-----
c       do conversion
c-----
        if(iiso.lt.0 .or.iiso.gt.1 )then
            WRITE(LER,*)'WRITE MODEL NOT ISOTROPIC OR TRANSVERSE',
     1          ' ISOTROPIC '
            stop
        endif
        if(ierr.lt.0)then
            if(ierr.eq.-1)WRITE(LER,*)'INPUT MODEL FILE DOES NOT EXIST'
            if(ierr.eq.-2)WRITE(LER,*)'INPUT IS NOT MODEL96 FILE'
            if(ierr.eq.-3)WRITE(LER,*)'ERROR IN   MODEL96 FILE'
            stop
        endif
        
c-----
c       force Transverse isotropic model
c-----
        iiso = 1
        mname = 'STDOUT'
        call putmod(1,mname,mmax,title(1:lt),iunit,iiso,iflsph,
     1          idimen,icnvel,.false.)
        end
