import boto3

def lambda_handler(event, context):
    """
    Lambda function to create an EMR cluster and add steps for processing data with Spark.
    """
    bucket_name = 'st0263-proyecto3'
    region = 'us-east-1'
    
    # Create a session with the specified region
    emr_client = boto3.client('emr')

    # Create the EMR cluster
    cluster_response = emr_client.run_job_flow(
        Name='Project3-Cloned',
        LogUri=f's3://{bucket_name}/elasticmapreduce',	
        ReleaseLabel='emr-7.3.0',
        Applications=[
            {'Name': 'HBase'},
            {'Name': 'HCatalog'},
            {'Name': 'Hadoop'},
            {'Name': 'Hive'},
            {'Name': 'Hue'},
            {'Name': 'JupyterHub'},
            {'Name': 'Spark'},
            {'Name': 'Sqoop'}
        ],
        Configurations=[
            {
                'Classification': 'spark-hive-site',
                'Properties': {
                    'hive.metastore.client.factory.class': 'com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory'
                }
            },
            {
              "Classification": "core-site",
              "Properties": {
                "fs.s3.consistent": "false"
              }
            }
        ],
        Instances={
            'InstanceGroups': [
                {
                    'Name': 'Core',
                    'Market': 'ON_DEMAND',
                    'InstanceRole': 'CORE',
                    'InstanceType': 'm5.xlarge',
                    'InstanceCount': 2,
                    'EbsConfiguration': {
                        'EbsBlockDeviceConfigs': [
                            {
                                'VolumeSpecification': {
                                    'VolumeType': 'gp2',
                                    'SizeInGB': 32
                                },
                                'VolumesPerInstance': 2
                            }
                        ]
                    }
                },
                {
                    'Name': 'Task - 1',
                    'Market': 'ON_DEMAND',
                    'InstanceRole': 'TASK',
                    'InstanceType': 'm5.xlarge',
                    'InstanceCount': 1,
                    'EbsConfiguration': {
                        'EbsBlockDeviceConfigs': [
                            {
                                'VolumeSpecification': {
                                    'VolumeType': 'gp2',
                                    'SizeInGB': 32
                                },
                                'VolumesPerInstance': 2
                            }
                        ]
                    }
                },
                {
                    'Name': 'Primary',
                    'Market': 'ON_DEMAND',
                    'InstanceRole': 'MASTER',
                    'InstanceType': 'm5.xlarge',
                    'InstanceCount': 1,
                    'EbsConfiguration': {
                        'EbsBlockDeviceConfigs': [
                            {
                                'VolumeSpecification': {
                                    'VolumeType': 'gp2',
                                    'SizeInGB': 32
                                },
                                'VolumesPerInstance': 2
                            }
                        ]
                    }
                }
            ],
            'Ec2KeyName': 'vockey',
            'KeepJobFlowAliveWhenNoSteps': False,
            'TerminationProtected': False,
            'EmrManagedMasterSecurityGroup': 'sg-02a314a7008e9e131',
            'EmrManagedSlaveSecurityGroup': 'sg-059776e19481dae34',
            'InstanceFleets': [],
            'Ec2SubnetIds': ['subnet-00b2bd144141a60bc']
        },
        EbsRootVolumeSize=32,
        VisibleToAllUsers=True,
        JobFlowRole='EMR_EC2_DefaultRole',
        ServiceRole='arn:aws:iam::296269837706:role/EMR_DefaultRole',
        AutoScalingRole='arn:aws:iam::296269837706:role/LabRole',
        ScaleDownBehavior='TERMINATE_AT_TASK_COMPLETION',
        Steps=[
            {
                'Name': 'addDependencies',
                'ActionOnFailure': 'TERMINATE_CLUSTER',
                'HadoopJarStep': {
                    'Jar': 's3://us-east-1.elasticmapreduce/libs/script-runner/script-runner.jar',
                    'Args': [f's3://{bucket_name}/scripts/dependencies.sh']
                }
            },
            {
                'Name': 'ETL',
                'ActionOnFailure': 'TERMINATE_CLUSTER',
                'HadoopJarStep': {
                    'Jar': 'command-runner.jar',
                    'Args': [
                        'spark-submit',
                        '--deploy-mode', 'cluster',
                        f's3://{bucket_name}/scripts/ETL.py',
                    ]
                }
            }
        ]
    )

    return {
        'statusCode': 200,
        'body': f"Clúster creado con ID: {cluster_response['JobFlowId']}"
    }