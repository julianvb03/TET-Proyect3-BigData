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
        LogUri=f's3://aws-logs-296269837706-us-east-1/elasticmapreduce',
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
            'KeepJobFlowAliveWhenNoSteps': True,
            'TerminationProtected': False,
            'EmrManagedMasterSecurityGroup': 'sg-02a314a7008e9e131',
            'EmrManagedSlaveSecurityGroup': 'sg-059776e19481dae34',
            'InstanceFleets': [],
            'Ec2SubnetIds': ['subnet-00b2bd144141a60bc']
        },
        EbsRootVolumeSize=32,
        VisibleToAllUsers=True,
        JobFlowRole='EMR_EC2_DefaultRole',
        ServiceRole='EMR_DefaultRole',
        AutoScalingRole='LabRole',
        ScaleDownBehavior='TERMINATE_AT_TASK_COMPLETION'
    )

    return {
        'statusCode': 200,
        'body': f"Clúster creado con ID: {cluster_response['JobFlowId']}"
    }
    
    # # Agregar los steps (procesamiento de Spark)
    # steps = [
    #     {
    #         'Name': 'ProcesarDatosSpark',
    #         'ActionOnFailure': 'CONTINUE',
    #         'HadoopJarStep': {
    #             'Jar': 'command-runner.jar',
    #             'Args': [
    #                 'spark-submit',
    #                 f's3://{bucket_name}/scripts/mi_script_spark.py',
    #                 bucket_name  # Parámetros adicionales, como el nombre del archivo
    #             ]
    #         }
    #     }
    # ]

    # # Ejecutar los steps en el clúster EMR
    # emr_client.add_job_flow_steps(JobFlowId=cluster_id, Steps=steps)
    # print("Steps añadidos al clúster.")