package io;

import java.io.FileWriter;
import java.io.IOException;

public class MyFileWriter2 extends FileWriter {

    public MyFileWriter2(String fileName) throws IOException {
        super(fileName);
        System.out.println("FileWriter 생성 = " + this);
    }

    @Override
    public void close() throws IOException {
        System.out.println("writer close() 호출 전2");
        throw new IOException("writer close 호출 중 예외 발생");
    }
}
