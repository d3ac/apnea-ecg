function isdone = step3()
    now_path = cd;
    fold=dir(strcat(now_path, '\step2 folder'));
    foldname={fold.name};
    Len = length(foldname);
    for i=3:1:Len
        cd(strcat(now_path, '\step2 folder'));
        str=string(foldname(1,i));
        name=char(str(1,1));
        mark=readcell(name);
        if isempty(mark)
            disp('pass');
            continue
        else
        n=width(mark);
        m=[];
        for j=2:2:n
            m=[m,j];
        end
        result=mark(:,m);
        cd(strcat(now_path, '\OSA RRi'))
        x=length(name);
        purename=name(1:x-4);
        newfold=strcat(purename,'.xlsx');
        xlswrite(newfold,result);
        end
    end
    isdone = 'step3 done';
end