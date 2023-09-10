import os
import pandas as pd
ae33keys=['Date','Time','Timebase',
        'RefCh1','Sen1Ch1','Sen2Ch1','RefCh2','Sen1Ch2','Sen2Ch2','RefCh3','Sen1Ch3','Sen2Ch3','RefCh4','Sen1Ch4','Sen2Ch4','RefCh5','Sen1Ch5','Sen2Ch5','RefCh6','Sen1Ch6','Sen2Ch6','RefCh7','Sen1Ch7','Sen2Ch7',
        'Flow1','Flow2','FlowC','Pressure(Pa)','Temperature(°C)','BB(%)','ContTemp','SupplyTemp','Status','ContStatus','DetectStatus','LedStatus','ValveStatus','LedTemp',
        'BC11','BC12','BC1','BC21','BC22','BC2','BC31','BC32','BC3','BC41','BC42','BC4','BC51','BC52','BC5','BC61','BC62','BC6','BC71','BC72','BC7',
        'K1','K2','K3','K4','K5','K6','K7','TapeAdvCount','ID_com1','ID_com2','ID_com3']
def read_ae33():
    file_dir = './AE33 0409-0426/'# where to read AE33 (.dat)
    files = os.listdir(file_dir)
    df1 = pd.read_table(os.path.join(file_dir, files[0]),skiprows=8,header=None,sep='\s+')  #read the first file
    for file in files[1:]:# continue to read other files
        df2 = pd.read_table(os.path.join(file_dir, file),skiprows=8,header=None,sep='\s+')
        df1 = pd.concat((df1, df2), axis=0, join='inner')
    df=df1
    del df2,df1
    
    df=df.reset_index(drop=True)
    df.columns=ae33keys
    df['Dateandtime']=df['Date']+' '+df['Time'] # connect date and time
    pd.to_datetime(df['Dateandtime'],format='%Y/%m/%d %H:%M:%S')
    # optional：use data on the hour
    df = df[df['Dateandtime'].apply(lambda x:x[-6:]==':00:00')]
    
    df=df.reset_index(drop=True)
    df['Dateandtime']=pd.to_datetime(df['Dateandtime'],format='%Y/%m/%d %H:%M:%S')
    # deal with BCX (unit conversion: ng/m3->μg/m3)
    for i in ['BC1','BC2','BC3','BC4','BC5','BC6','BC7']:
        df[i]=df[i]/1000     
    return df