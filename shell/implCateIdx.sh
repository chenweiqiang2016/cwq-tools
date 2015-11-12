#!/bin/bash

if [ $# -lt 3 ];then
	echo "Usage: $0 filename countPerPage outFilename";
	exit 1;
fi

filename=$1
base=$2
outFilename=$3


awk -F "\t" 'BEGIN {getline; for(i=1;i<NF+1;i++){\
                                 if($i=="page"){\
                                     page_idx=i;}
                                 else if($i=="position"){
                                     pos_idx=i}}; 
                   print $0 "\t" "category_index";}\
{print $0 "\t" ($page_idx-1)*countPerPage + $pos_idx;}\
END{}' countPerPage=$base $filename\
> $outFilename
