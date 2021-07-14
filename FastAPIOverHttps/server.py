import uvicorn

if __name__ == '__main__':
    uvicorn.run("main:app",
                port=8432,
                reload=True,
                )