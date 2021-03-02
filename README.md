# tagValidationCode
Code for ECAL tag validation

## Get the code

First, fork the repository [here](https://github.com/cippy/tagValidationCode) into your github area
Then
```
export SCRAM_ARCH="slc7_amd64_gcc900"
cmsrel CMSSW_11_3_0_pre3
cd CMSSW_11_3_0_pre3/src
cmsenv
git cms-init
YOUR_GITHUB_REPOSITORY=$(git config user.github) # set it by hand if it doesn't work
git clone https://github.com/cippy/tagValidationCode.git -b main TagValidationCode/core/
cd TagValidationCode/
git remote add origin git@github.com:$YOUR_GITHUB_REPOSITORY/tagValidationCode.git
git push -u origin main
cd $CMSSW_BASE/src && scram b -j 8
```

## Use the code

Requires python 3, which can be called as `python3` (default in CMSSW is probably python 2.7.x)
```
python3 ecalTagValidator.py [-h]
```
See options inside or using -h for help
