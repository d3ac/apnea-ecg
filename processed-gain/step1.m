function isdone = step1(path)
    %dir('.')列出当前目录下所有子文件夹和文件%
    excel_path = path;   %文件夹路径 
    img_path_list = dir(strcat(excel_path,'*.xlsx'));     
    %文件的长度
    img_num = length(img_path_list);
    for i=1:img_num
        file_path = [excel_path img_path_list(i).name];
    %% 读取HRV
    %% 设置导入选项并导入数据
    opts = spreadsheetImportOptions("NumVariables", 4);
    % 指定工作表和范围
    opts.Sheet = "气流事件";
    opts.DataRange = "A9";
    % 指定列名称和类型
    opts.VariableNames = ["SignalID", "FlowDflow", "VarName3", "VarName4"];
    opts.VariableTypes = ["datetime", "datetime", "double", "string"];
    % 指定变量属性
    opts = setvaropts(opts, "VarName4", "WhitespaceRule", "preserve");
    opts = setvaropts(opts, "VarName4", "EmptyFieldRule", "auto");
    opts = setvaropts(opts, "SignalID", "InputFormat", "");
    opts = setvaropts(opts, "FlowDflow", "InputFormat", "");
    T = readtable(file_path, opts, "UseExcel", false);
    %% 清除临时变量
    clear opts
    OSA_begin = T.SignalID;
    OSA_end = T.FlowDflow;
    OSA_duration = T.VarName3;
    OSA_type = T.VarName4;
    %% 读取HRV
    %% 设置导入选项并导入数据
    opts = spreadsheetImportOptions("NumVariables", 4);
    % 指定工作表和范围
    opts.Sheet = "RR间期";
    opts.DataRange = "A9";
    % 指定列名称和类型
    opts.VariableNames = ["SignalID", "Value"];
    opts.VariableTypes = ["datetime", "double"];
    % 指定变量属性
    opts = setvaropts(opts, "SignalID", "InputFormat", "");
    T = readtable(file_path, opts, "UseExcel", false);
    %% 清除临时变量
    clear opts
    HR_start = T.SignalID;
    HR_val = T.Value;
    
    OSA_begin_second = zeros(length(OSA_begin),1);
    for i=1:size(OSA_begin,1)
	    time_t = datevec(OSA_begin(i,1));
        if(time_t(4)<=12)
            time_t(4) = time_t(4) + 24;
        end
        OSA_begin_second(i) = time_t(4)*3600+time_t(5)*60+time_t(6);
    end
    
    OSA_end_second = zeros(length(OSA_end),1);
    for i=1:size(OSA_end,1)
	    time_t = datevec(OSA_end(i,1));
        if(time_t(4)<=12)
            time_t(4) = time_t(4) + 24;
        end
        OSA_end_second(i) = time_t(4)*3600+time_t(5)*60+time_t(6);
    end
    
    HR_start_second = zeros(length(HR_start),1);
    for i=1:size(HR_start,1)
	    time_t = datevec(HR_start(i,1));
        if(time_t(4)<=12)
            time_t(4) = time_t(4) + 24;
        end
        HR_start_second(i) = time_t(4)*3600+time_t(5)*60+time_t(6);
    end
    
    line = 1;
    write1 = [];
    for i=1:size(OSA_begin,1)
	    for j = line:size(HR_start,1)
           if(isnan(HR_val(j)))
               write1 = [write1;2];
           elseif(HR_start_second(j)>=OSA_begin_second(i)&&HR_start_second(j)<=OSA_end_second(i))
               write1 = [write1;1];
           elseif(HR_start_second(j)<OSA_end_second(i))
               write1 = [write1;0];
           else
               line = j;
               break;
           end
        end
    end
    
    for k = line:size(HR_start,1)
        write1 = [write1;0];
    end
    xlrow = num2str(size(HR_start,1)+8);
    xlRange = ['C9:C',xlrow];
    xlswrite(file_path,write1,'RR间期',xlRange);
    end
    isdone = 'step1 done';
end
