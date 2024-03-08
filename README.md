# Galaxy Life: Pocket Adventures Server
This repository contains all the code relative to Galaxy Life Pocket Adventures Server.  
If there is a large enough desire for a commercial server ran by Phoenix Network, we will consider it of there is funding to support it. We are currently (March 2024 and onwards) focusing on the Unreal Engine port for mobile instead of continuing work on Pocket Adventures.

If ever we obtain more resources and financial stability, we might look into further developing this project.

## Licensing
The license (Business Source License 1.1) can be found in `LICENSE.md`. This code can **NOT** be used for production or commercial purposes. It is purely here for those who want to tinker or play with the old Pocket Adventures while we are working to release our mobile version with Unreal Engine!

If Phoenix Network (the licensor) ever goes under or stops working on any Galaxy Life related product, this project will receive an MIT license.

## Setup
### Install dependencies
Install needed modules using the following command:
> python -m pip install -r requirements.txt

### Create the database
Edit DATABASE_URI in config.py if needed then enter the following command to create db schema
> flask db init

> flask db migrate

> flask db upgrade

## Running the backend
Either run it using:
> python app.py 

Or setup the backend using a WSGI server if you are running it in prod
