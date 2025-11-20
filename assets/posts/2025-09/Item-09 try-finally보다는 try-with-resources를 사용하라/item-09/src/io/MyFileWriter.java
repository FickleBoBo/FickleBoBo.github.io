package io;

import java.io.FileWriter;
import java.io.IOException;

// FileWriter 클래스를 상속 받아 자원 생성, 회수 출력 로직만 추가
public class MyFileWriter extends FileWriter {

    public MyFileWriter(String fileName) throws IOException {
        super(fileName);
        System.out.println("FileWriter 생성 = " + this);
    }

    @Override
    public void close() throws IOException {
        System.out.println("writer close() 호출 전");
        super.close();
        System.out.println("writer close() 호출 후");
    }
}
