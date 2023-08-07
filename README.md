LIGHTPARTICLE - Backup your online data for "read-it-offline" | [简体中文](README-ZH_CN.md)

- No additional external module dependencies.
- No need databased (file-flatted).
- Abundant configuration parameters.

## Usage

Download the source code of this project and switch to this directory:

> ./LIGHTPARTICAL

For more usage options, refer to the [settings.py](settings.py) file.
We do not provide any 'out-of-the-box' tools or programs free of charge, due to 
concerns about uncertainty about specific uses.

## Directory

```
LIGHTPARTICLE                             # Project $HOMEDIR$
├── doc                                   # Manuals and APIDoc by `pdoc`
├── libmweb-linux-2.40.0                  # MWeb library for Linux
├── static                                # Static resource(s)
│   ├── certs                             # Local Service HTTPS certs.
│   ├── data                              # Default storage path for online data
│   └── www                               # Frontend (*.html; *.js; etc.) Path
| ...(omit)...                            # LIGHTPARTICLE modules
└── testing                               # Testcase and batch executor

```

The dynamically configurable parameters 'basedir' and 'dirname' are already 
provided in the code to specify the directory structure where static resource 
files are stored. According to actual needs, the directory structure can be 
designed to facilitate subsequent data analysis and operation.

## Testing
To facilitate testing, we designed and implemented a simple unit test execution 
module. About existing test cases, test case writing methods, For details such 
as use case registration and batch execution, please refer to the files in the 
[Document](doc) directory.

## Development

Even if we use a native implementation that only relies on Python as much as 
possible, we avoid the heavy use of third-party modules and simplify the 
installation and deployment. 

In the actual development process, it is still recommended to install the code 
analysis tools and modules provided by PyCharm. In order to clearly understand 
part of the relationships between code blocks, dynamic debugging at runtime.

TThe following features are built separately by us and may cause some confusion 
in actual debugging when encountering problems:

- Replace the encapsulation of the logging module to provide simplified log 
  output 'utility.bl4th3r(level, msg)'  

  - Blocking  
  - No file-handler is provided to output logs to a file  
  - Log level may change the running state of the program   
    - (e.g. 'critical' triggers 'SystemExit' to terminate execution)  
  - Lack of more efficient filtering options and verbose output  
 
- Avoid the additional learning cost of learning about unittest and provide 
  [testing.py](testing/testing.py) tools  

  - Deep level exceptions triggered in use cases may not be thrown due to the 
    use of exception handling to prompt and handle 'testcases' that cannot be 
    found

- The request processing part adopts a C/Python mix
  
  - This part is not open source and debugging is difficult
  - The provided binary file compilation parameters do not add debugging-related 
    configuration, and the library file cannot be directly debugged  
  - Even if it has been built using a full-static method, there will still be 
    other unknown exceptions including system compatibility issues  

Any form of PR is welcome to share your ideas.  

## Disclamer

You may need to use the codes and modules in this project to write the 
operations you need. The content of the code created by you has nothing to do 
with the organization, and we do not assume any additional responsibility for 
your creation, your subsequent behavior, and will not provide further technical 
support.

The tool is not an official application, and the methods provided in the code 
may not be available due to subsequent version updates of the official platform 
application.

In accordance with the requirements of the "Platform" (*.zsxq.com) rules, even 
if you use the code in this repository to build the required functionality, any 
purchased data downloaded by you can only be used for your personal offline 
reading and browsing use. Do not infringe on the rights and interests of the 
content publisher's platform, "any download is recorded", and republish of data 
content that you have paid for but only has browsing rights is not allowed by 
the "Platform".
