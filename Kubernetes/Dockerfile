FROM python:3


# Set working directory to use
WORKDIR /app


# install dependencies
RUN pip install streamlit
RUN pip install --upgrade google-cloud-firestore
RUN pip install --upgrade google-cloud-storage


# expose port for streamlit to work
EXPOSE 8501


# Copy our app from the current directory to the working area.
COPY . /app


# create an entry point to make our image executable.
ENTRYPOINT ["streamlit", "run"]


# run the application
CMD ["frontend.py"]