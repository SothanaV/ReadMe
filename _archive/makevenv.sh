#!/bin/sh
env_name=${1-env}
python_version=${2-python3}

if [ -f ~/bin/venv/${env_name} ]; then
	echo "${env_name} already install, please check in ~/env";
else
	if ! [ -x "$(command -v virtualenv)" ]; then
	  echo 'install virtualenv' >&2
	  sudo apt-get install virtualenv
	fi
	if [ ! -d "env" ]; then
	    echo "- Create user ~/env directory"
	    mkdir ~/env
	fi
	if [ ! -d "bin" ]; then
	    echo "- Create user ~/bin directory"
	    mkdir ~/bin
	fi
	if [ ! -d "bin/venv" ]; then
	    echo "- Create user ~/bin/venv directory"
	    mkdir ~/bin/venv
	fi

	echo "create ${env_name} enviroment with ${python_version}"
	cd ~/env
	virtualenv -p ${python_version} ${env_name}
	
	echo "Register ${env_name} to bin"
	cd ..
	echo -e "#!/bin/bash\nsource ~/env/${env_name}/bin/activate" >> ~/bin/venv/${env_name}
	
	echo ""
	echo "Make virtual evniroment complete."
	echo ""
	
	if grep -Fwq 'export PATH="~/bin/venv:$PATH' ~/.bashrc; then
		:
	else
		echo ""
		echo -e '\nexport PATH="~/bin/venv:$PATH"' >> ~/.bashrc;
		echo "###############################################"
		echo ""
		echo " Please re-open session to activate enviroment."
		echo ""
		echo "###############################################"
		echo ""
	fi

	echo ""
	echo " Use following command to activate "
	echo ""
	echo " > source ${env_name}"
	echo ""
fi