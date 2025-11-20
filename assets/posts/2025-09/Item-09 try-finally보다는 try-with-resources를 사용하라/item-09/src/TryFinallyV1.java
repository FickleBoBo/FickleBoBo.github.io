import io.MyFileReader;

import java.io.BufferedReader;
import java.io.IOException;

public class TryFinallyV1 {

    public static void main(String[] args) {
        try {
            System.out.println(firstLineOfFileV1("resources/data.txt"));
            // FileReader 생성 = io.MyFileReader@10f87f48
            // reader close() 호출 전
            // reader close() 호출 후
            // abc
        } catch (IOException e) {
            e.printStackTrace();
        }

        try {
            System.out.println(firstLineOfFileV1("resources/data.dat"));
        } catch (IOException e) {
            e.printStackTrace();
            // FileReader 생성 = io.MyFileReader@4e50df2e
            // java.io.IOException: firstLineOfFileV1 .dat 파일 확장자 예외
            //     at TryFinallyV1.firstLineOfFileV1(TryFinallyV1.java:59)
            //     at TryFinallyV1.main(TryFinallyV1.java:20)
            // -> 예외가 터지며 자원 회수 실패
        }

        try {
            System.out.println(firstLineOfFileV2("resources/data.txt"));
            // FileReader 생성 = io.MyFileReader@6e8cf4c6
            // reader close() 호출 전
            // reader close() 호출 후
            // abc
        } catch (IOException e) {
            e.printStackTrace();
        }

        try {
            System.out.println(firstLineOfFileV2("resources/data.dat"));
        } catch (IOException e) {
            e.printStackTrace();
            // FileReader 생성 = io.MyFileReader@12edcd21
            // reader close() 호출 전
            // reader close() 호출 후
            // java.io.IOException: firstLineOfFileV2 .dat 파일 확장자 예외
            //     at TryFinallyV1.firstLineOfFileV2(TryFinallyV1.java:76)
            //     at TryFinallyV1.main(TryFinallyV1.java:41)
            // -> 예외가 터졌지만 자원 회수 성공
        }
    }

    static String firstLineOfFileV1(String path) throws IOException {
        BufferedReader br = new BufferedReader(new MyFileReader(path));

        // .dat 확장자면 예외를 던짐
        if (path.endsWith(".dat")) {
            throw new IOException("firstLineOfFileV1 .dat 파일 확장자 예외");
        }

        String line = br.readLine();

        // 자원 회수
        br.close();

        return line;
    }

    static String firstLineOfFileV2(String path) throws IOException {
        BufferedReader br = new BufferedReader(new MyFileReader(path));

        try {
            // .dat 확장자면 예외를 던짐
            if (path.endsWith(".dat")) {
                throw new IOException("firstLineOfFileV2 .dat 파일 확장자 예외");
            }

            return br.readLine();
        } finally {
            // 자원 회수
            br.close();
        }
    }
}
