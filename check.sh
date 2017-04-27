#!/bin/bash
green='\033[0;32m';
red='\033[0;31m';
nc='\033[0m';

cont=true

diff_filter(){
	#diff -y -W 150 --suppress-common-lines $1 $2 | sed -e 's/\s*<[^>]*>//g';
	diff $1 $2 | sed -e 's/\s*<[^>]*>//g';
}


while true;
do
	wget http://www.or.uni-bonn.de/lectures/ss17/appr_ss17.html &> /dev/null;
	wget http://www.or.uni-bonn.de/lectures/ss17/appr_ss17_ex.html &> /dev/null;
	wget http://www.math.uni-bonn.de/ag/logik/teaching/2017SS/Models_of_set_theory_1.shtml &> /dev/null;
	wget http://www.math.uni-bonn.de/ag/ana/SoSe2017/weights/index.html &> /dev/null;

	wifile=index_crop.html;
	wifile_old=$wifile"_old";

	cat index.html | grep '<div\sid=\"col1_content\"' -m 1 -A 999 | grep '</div>' -m 1 -B 999 > $wifile;
	rm index.html;

	aafile=appr_ss17.html;
	aafile_old=$aafile"_old";

	aefile=appr_ss17_ex.html;
	aefile_old=$aefile"_old";

	msfile=Models_of_set_theory_1.shtml;
	msfile_old=$msfile"_old";

	aadiff="$(diff_filter $aafile_old $aafile)";
	aediff="$(diff_filter $aefile_old $aefile)";
	msdiff="$(diff_filter $msfile_old $msfile)";
	widiff="$(diff_filter $wifile_old $wifile)";

	if [ "$aadiff" != "" ]
	then printf "${green} APPROXIMATION ALGORITHMS lec!${nc}\n$aadiff\n";
	fi

	if [ "$aediff" != "" ]
	then printf "${green} APPROXIMATION ALGORITHMS ex!${nc}\n$aediff\n";
	fi

	if [ "$msdiff" != "" ]
	then printf "${green} SET THEORY!${nc}\n$msdiff\n";
	fi

	if [ "$widiff" != "" ]
	then printf "${green} WEIGHTED INEQUALITIES!${nc}\n$widiff\n";
	fi

	mv $msfile $msfile_old;
	mv $aafile $aafile_old;
	mv $aefile $aefile_old;
	mv $wifile $wifile_old;

	printf "${red} checked ${nc}\n";
	sleep 500;
done
