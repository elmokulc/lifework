# Update docker image

If you need to update the **environment.yml**. You can also create an associate docker image and use it for the CI run. 

1. Update **environment.yml** with yours modules.
   - ***Warning***: Don't forget to include *Jupyter-book* module

            conda install -c conda-forge jupyter-book

    - Export a conda environment:
        
            conda activate "your_env_name"
            conda env export | sed 's/name: .*/name: base/'  | sed 's/prefix: .*//' > environment.yml

    
      **Note**: We make sure that environment name is ***"base"***

2. Build your docker image.

        docker build -t <image_name>:<tag_name> <path_to_Dockerfile> <path_to_your_dockerfile>
   
    - Example with my DockerHub account. Current directory is **positron/**.

            docker build -t celmo/jupyter-book:latest .

# Test gitlab-ci locally  
If you want to check your work locally follow this.

1. Install gitlab-runner, see [here](https://docs.gitlab.com/runner/install/)

3. Update **image** section of **.gitlab-ci.yml** with your docker image name.
    - Example: 
    
            jupyter-build:
                stage: build
                image: celmo/jupyter-book

4. Run the following command:
        
        sudo gitlab-runner exec docker --docker-pull-policy=never jupyter-build

    **Note**: *"--docker-pull-policy=never"* argument allows you to use your local docker image whitout pushing your image on DockerHub.


# Push your docker image

1. Having a DockerHub account see [here](https://docs.docker.com/docker-hub/)
2. Run the following command:
        
        docker push <image_name>:<tag_name>

    Example:
    
        docker push celmo/jupyter-book:latest 

3. Clean :

        docker system prune -a -f

# Use Gitlab container registry 

You may want to use the Gitlab container registry to store docker images and to use it for your repository instead of using DockerHub , see more explanantions [here](https://about.gitlab.com/blog/2016/05/23/gitlab-container-registry/).

1. Log Gitlab registry with docker: 

    if first time:

        docker login registry.gitlab.com -u <your_account> -p <your_token>

    else: 
    
        docker login registry.gitlab.com

2. Build image:

        docker build -t registry.gitlab.com/celmo/lifework .

3. Push Image:

        docker push registry.gitlab.com/celmo/lifework:latest

4. Update **.gitlab-ci.yml** with your new image.

    Example:

        stages:
           - build
           - deploy

        jupyter-build:
            stage: build
            image: registry.gitlab.com/symmehub/teaching/positron:latest

# Use Github container registry 

1. Log to Github registry with docker:

    - Create personal access token for the command line see [here](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line)
   
    - Save your PAT as an environment variable.

            export CR_PAT=YOUR_TOKEN

    - Using the CLI for your container type, sign in to the Container registry service at ghcr.io.

            echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin
            Login Succeeded

2. Build your container image properly:
    
    Example:

            docker build -t ghcr.io/elmokulc/lifework:latest .


3. Push container to GitHub registry:
    
            docker push ghcr.io/elmokulc/lifework:latest

4. Optionnal inspect:

            docker inspect ghcr.io/symmehub/positron/positron:latest
