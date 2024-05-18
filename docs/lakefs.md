# LakeFS


Prepare Docker compose [image](../lakefs/docker-compose.yml) and using local lakefs storage running [Snakefile](../Snakefile)

## Configuration Lake FS

Running Docker compose:

`cd lakefs`
`docker-compose up`

then download credential with
1) access_key_id: ********************
2) secret_access_key: ******************

`docker exec -it -u 0 lakefs-dz-lakefs-1 sh `

`lakectl config` (specify the secrets that LakeFS has deduced while download credentials)

## running snakefile

`snakemake --cores all`

In this pipeline realize upload and download artifacts from local lakefs storage with command

`lakectl fs upload`
`lakectl fs download`