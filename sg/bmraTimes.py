import datetime as dt
import pytz


""" This is a set of objects and functions for comparing times which cross trading period boundaries in the BMRA. 
    
    Times and periods in the BM are defined either in GMT, or in Settlment Day + settlement Period
    BST times are never used 'raw' within the bm, but there is the opportunity for confusion where times are only defined by Settlement day and period. 
    
    One other complication is that a time returned from the Mysql database is stored as a 
    deltTime object rather than a pure time. 
    
    OBJECT definition
    
    bmra_dt is an object which stores a time with the following properties: 
        - sd(Settlment Day - This changes at <local> midnight)
        - sp(settlment Period - Usually 1 - 48, but 1 - 46 on clock forward day and 1 - 50 on clock back day)
        - datetTime(Date time in GMT)
        - sp_datetime (Start of the settlment period in GMT) 
        - tz (time zone: either 0 = GMT, 1 = BST, -1 = Clock Forward Day, -2 = clock Back Day)
    
    a bmra_dt object can be initialised in the following ways: 
        1. A single date-time object in GMT. 
        2. A settlment Day and settlment Period, the value of the objects datetime will be the same as the start of the period
        3. A  settlment Day and settlment period object and a time delta object representing the number of seconds from the start of that settlement period. 
    
    The following methods are include: 
        i.      pprint() - to pretty print the object
        ii.     datetimeAdjust() - takes in a raw time and a direction (1: GMT -> BST 2: BST -> GMT) - and corrects the time only if a correction is required i.e. looks to see if current date is part of BST or GMT
        iii.    whatTimeZone() : Returns a flag to identify if day is GMT, BST, clock forward day or clock back day
        iv.     spRangeCheck(): Returns the number of settlement periods for a given date (normally 48, but 46 or 50 on clock change days)
        v.      spList(): Returns 4 lists which give the settlment day, period and start to of GMT of all periods between two dates (inclusive). Accounting for clock change days
        vi.     interpolate(): Returns list of bmraDT objects for start and end times and at each period change in between. And returns list of linear interpolation between the input start and end level 
        
"""


class bmraDT:
    
    def __init__(self, sd, sp, datetime, sp_datetime, tz):
        self.sd = sd
        self.sp = sp
        self.datetime = datetime        
        self.sp_datetime = sp_datetime
        self.tz = tz
    
    """ This is a BMRA date-time object which as well as a date and a time includes information on the 
        trading period in which the time occures
    """
    ##############################
    ## Class method to define   ##
    ## a bmdt object from a     ##
    ## datetime object in GMT   ##
    ##############################
    
    @classmethod
    def from_dt(cls,datetime):
        
        # Adjusted time is in local time - either GMT or BST
        adjusted_datetime = bmraDT.datetimeAdjust(datetime, 1)

        #Date of adjusted time for settlement day 
        sd = adjusted_datetime.date()
        
        #The time zone: either GMT, BST, clocks forward day or clocks back day [0, 1, -1, -2]. 
        tz = bmraDT.whatTimeZone(datetime)
        
        #calculate settlement period containting datetime
        if tz >= 0:
            #If not a clock change day calculate period based on adjusted time which is in correct of GMT, BST
            sp = (adjusted_datetime.time().hour*2) + 1  + int(adjusted_datetime.time().minute/30)
        elif tz == -1: 
            # If clock forward day...
            if datetime.hour <23:
                #Period 47 am 48 disapear... And the next settlement day starts at 23:00
                sp = (datetime.time().hour*2) + 1  + int(datetime.time().minute/30)
            else: 
                sp = (adjusted_datetime.time().hour*2) + 1  + int(adjusted_datetime.time().minute/30)
        elif tz == -2:
            # If clocks backward day... two extra periods: 49 and 50 and the next settlment day starts at 00:00
            if adjusted_datetime.hour <= 2:
                sp = (adjusted_datetime.time().hour*2) + 1  + int(adjusted_datetime.time().minute/30)
            else:
                sp = (adjusted_datetime.time().hour*2) + 1  + int(adjusted_datetime.time().minute/30) + 2
            
        #Date time in GMT of the start of the settlement period
        sp_datetime = dt.datetime.combine(datetime.date(), dt.time(datetime.hour, 30*((sp-1)%2)))
                
        bmradt = cls(sd,sp, datetime, sp_datetime, tz)
        
        return bmradt

    ##############################
    ## Class method to define   ##
    ## a bmdt object from a     ##
    ## settlement day and       ##
    ## settlement period        ##
    ##############################
        
    @classmethod
    def from_dp(cls,sd, sp):
        
        #First check if sp is in correct range:
        sp_check = bmraDT.spRangeCheck(sd, sp)
        
        if sp_check == 0 :
            print('Settlment Period number invalid')
            return
        
        
        #Calculate the date time of start of period in BST or GMT
        if sp <= 48:
            adjusted_dt = dt.datetime.combine(sd, dt.time(int((sp-1)/2), 30*((sp-1)%2)))
        else:
            adjusted_dt = dt.datetime.combine(sd, dt.time(int((48-1)/2), 30*((48-1)%2)))
 
            adjusted_dt += dt.timedelta(seconds=((sp-48)*1800))

        
        tz = bmraDT.whatTimeZone(adjusted_dt)
        

        
        if tz == -1: 
            #Bug fix to deal with post clock change times on the clock forward day
            datetime = adjusted_dt
        else:
            datetime = bmraDT.datetimeAdjust(adjusted_dt, -1)

        #Bug fix for two hours which under system creep out of the clock change day 
        if sp >= 49: tz = -2

        if tz == -2 and sp > 2: 
            # adjustment for the clock back day
            datetime -= dt.timedelta(seconds=3600)

        bmradt = cls(sd, sp, datetime, datetime, tz)
        
        return bmradt
        
        
        
    ##############################
    ## Class method to define   ##
    ## a bmdt object from a     ##
    ## settlement day and       ##
    ## settlement period  and   ##
    ## a time delta object      ##
    ##############################
        
    @classmethod
    def from_dpdt(cls,sd, sp, td):
        
        #First check if sp is in correct range:
        sp_check = bmraDT.spRangeCheck(sd, sp)
        
        if sp_check == 0 :
            print('Settlment Period number invalid')
            return
        
        
        #Calculate the date time of start of period in BST or GMT
        if sp <= 48:
            adjusted_dt = dt.datetime.combine(sd, dt.time(int((sp-1)/2), 30*((sp-1)%2)))
        else:
            adjusted_dt = dt.datetime.combine(sd, dt.time(int((48-1)/2), 30*((48-1)%2)))
 
            adjusted_dt += dt.timedelta(seconds=((sp-48)*1800))

        
        tz = bmraDT.whatTimeZone(adjusted_dt)
        

        
        if tz == -1: 
            #Bug fix to deal with post clock change times on the clock forward day
            sp_datetime = adjusted_dt
        else:
            sp_datetime = bmraDT.datetimeAdjust(adjusted_dt, -1)

        #Bug fix for two hours which under system creep out of the clock change day 
        if sp >= 49: tz = -2

        if tz == -2 and sp > 2: 
            # adjustment for the clock back day
            sp_datetime -= dt.timedelta(seconds=3600)

        # Now add in the time delta as an increase from midnight GMT
        
        
        
        if td.seconds == 0 and sp_datetime.time() == dt.time(23,30):
            datetime = dt.datetime.combine(sp_datetime.date(), dt.time(0,0)) + dt.timedelta(days=1)
        else:
            datetime = dt.datetime.combine(sp_datetime.date(), dt.time(0,0))+td

        bmradt = cls(sd, sp, datetime, sp_datetime, tz)
        
        return bmradt        


    ##############################
    ## Method to pretty print a ##
    ## a bmdt object            ##
    ##############################        
        
    def pprint(self):
        print('Date Time:           '+str(self.datetime)+' GMT')
        print('Settlement Day:      '+str(self.sd))
        print('Settlement Period:   '+str(self.sp))
        print('Start of SP:         '+str(self.sp_datetime)+' GMT')
        if self.tz == 0: tz_code = 'GMT'
        elif self.tz == 1: tz_code = 'BST'
        elif self.tz == -1: tz_code = 'Clocks Forward Day'
        elif self.tz == -2: tz_code = 'Clocks Back Day'
        
        print('Time Zone:           '+tz_code)
        
    ##############################
    ## Method to adjust between ##
    ## GMT and Local (GMT/BST)  ##
    ##############################   
        
    def datetimeAdjust(datetime, direction):
        bst = pytz.timezone('Europe/London')
        if direction == 1: 
            #Input is GMT, output is either GMT or BST
            return(pytz.utc.localize(datetime).astimezone(bst))
        if direction == -1:
            #Input is either GMT or BST, output is GMT
            return(bst.localize(datetime).astimezone(pytz.utc))

    ##############################
    ## Method to identify if day##
    ## is BST, GMT or a clock   ##
    ## change day               ##
    ##############################   
        
    def whatTimeZone(datetime):
        if type(datetime) is dt.datetime:
            ddate = datetime.date()
        else:
            ddate = datetime
        
        bst = pytz.timezone('Europe/London')
        if ddate in [x.date() for x in bst._utc_transition_times]:
      
            if ddate.month  == 3:
                tz = -1
            elif ddate.month == 10 :
                tz = -2
        else:
            dls = bst.localize(dt.datetime.combine(ddate, dt.time(0,0))).dst().seconds
            
            if dls== 3600 : tz = 1
            else: tz = 0
        
        return tz
        
    ##############################
    ## Method to check if sp in ##
    ## range allowed            ##
    ##############################   
    
    def spRangeCheck(sd, sp):
        
        bst = pytz.timezone('Europe/London')
        #Initial flag variable
        check = 0
        #Upper limit
        ul = 48
        #Only do detailed check for dates in March and october
        if sd.month in [3, 10]: 
            #Check if date is a clock change day
            if sd in [x.date() for x in bst._utc_transition_times]:
            #And adjust upper limit acordingly
                if sd.month == 3: ul = 46 
                if sd.month == 10: ul = 50
        
        if sp >= 1 and sp <= ul:
            check = 1
        return check, ul
        
    ##############################
    ## Method produce lists of  ##
    ## time-series to cover all ##
    ## sps between two dates    ##
    ## (inclusive)              ##
    ##############################   

    def spList(sDate, eDate):
        
        #Create list of dates
        
        
        dList = []
        for x in range((eDate-sDate).days+1):
            dList.append((dt.datetime.combine(sDate,dt.time(0,0))+dt.timedelta(days=x)).date())
        
        dTimeSeries = []
        pTimeSeries = []
        dtTimeSeries = []
        for d in dList: 
            c, ul = bmraDT.spRangeCheck(d, 1)
            for u in range(ul):
                dTimeSeries.append(d)
                pTimeSeries.append(u+1)
                dtTimeSeries.append(bmraDT.from_dp(d,u+1).datetime.replace(tzinfo=None))
    
        return dList, dTimeSeries, pTimeSeries, dtTimeSeries


    def interpolate(st, sl, et, el):
        """ Input should be in the form of two bmraDTs and two 'level' which for example represent power
            Ouptut will be two time serries inclusive of the origianl point, and with additional points
            added at the internal settlment period start/end points. 
            The additional points are calculated by linear interpolation.
            The times returned are in bmraDT format
        """
        
        if st.sd == et.sd and st.sp == et.sp:
            #If the two points are in the same period 
            return [st, et], [sl, el]
        else:
            # Number of periods crossed (Use period start times to avoid issues with clock changes)
            np = int(1+((et.sp_datetime - st.sp_datetime).seconds + (et.sp_datetime - st.sp_datetime).days*24*60*60)/(30*60))
            
            #get time-values for interpolated series
            tInt = [st]
            tIntSec = [0]
            levelInt = [sl]
            totalTimeSeconds= (et.datetime -st.datetime).seconds + (et.datetime -st.datetime).days*24*60*60
            
            for n in range(1,np):
                tInt.append(bmraDT.from_dt(st.sp_datetime+dt.timedelta(minutes=30*n)))
                tIntSec.append(1800 - (st.datetime - st.sp_datetime).seconds + (n-1)*30*60)
                
                levelInt.append(sl + ((el-sl)* (tIntSec[-1] / totalTimeSeconds)))
            
            tInt.append(et)
            tIntSec.append(totalTimeSeconds)
            levelInt.append(el)
            
            
            return tInt, levelInt
                

def noOfPeriods(sd):
        
        bst = pytz.timezone('Europe/London')
        #default
        n = 48
        #Only do detailed check for dates in March and october
        if sd.month in [3, 10]: 
            #Check if date is a clock change day
            if sd in [x.date() for x in bst._utc_transition_times]:
            #And adjust upper limit acordingly
                if sd.month == 3: n = 46 
                if sd.month == 10: n = 50
        return n
