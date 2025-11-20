package io;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

// FileReader 클래스를 상속 받아 자원 생성, 회수 출력 로직만 추가
public class MyFileReader extends FileReader {

    public MyFileReader(String fileName) throws FileNotFoundException {
        super(fileName);
        System.out.println("FileReader 생성 = " + this);
    }

    @Override
    public void close() throws IOException {
        System.out.println("reader close() 호출 전");
        super.close();
        System.out.println("reader close() 호출 후");
    }
}
