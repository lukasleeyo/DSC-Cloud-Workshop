# FROM scratch if not importing an image
FROM python:3


# using pip to install streamlit library
RUN pip install streamlit



# Set working directory as "app"
WORKDIR /app

# Copy our "app.py" to the working directory
COPY ./app.py /app



# expose port 8501 for streamlit
EXPOSE 8501



# create an entry point to make our image executable
ENTRYPOINT ["streamlit", "run"]

# run the application -> [ENTRYPOINT] [CMD] -> "streamlit run app.py"
CMD ["app.py"]
