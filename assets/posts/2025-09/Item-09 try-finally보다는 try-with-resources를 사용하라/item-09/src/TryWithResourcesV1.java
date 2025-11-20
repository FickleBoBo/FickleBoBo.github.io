import io.MyFileReader;
import io.MyFileWriter;
import io.MyFileWriter2;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;

public class TryWithResourcesV1 {

    public static void main(String[] args) {
        try {
            System.out.println(copyV3("resources/data.txt", "resources/dataV3.txt"));
            // FileReader 생성 = io.MyFileReader@10f87f48
            // FileWriter 생성 = io.MyFileWriter@7291c18f
            // writer close() 호출 전
            // writer close() 호출 후
            // reader close() 호출 전
            // reader close() 호출 후
            // ok
            // -> try-with-resources 구문에서 명시한 순서의 반대 순서로 닫아줌
        } catch (IOException e) {
            e.printStackTrace();
        }

        try {
            System.out.println(copyV3("resources/data.dat", "resources/dataV3.dat"));
        } catch (IOException e) {
            e.printStackTrace();
            // FileReader 생성 = io.MyFileReader@7cc355be
            // FileWriter 생성 = io.MyFileWriter@6e8cf4c6
            // writer close() 호출 전
            // writer close() 호출 후
            // reader close() 호출 전
            // reader close() 호출 후
            // java.io.IOException: copyV3 .dat 파일 확장자 예외
            //     at TryWithResourcesV1.copyV3(TryWithResourcesV1.java:70)
            //     at TryWithResourcesV1.main(TryWithResourcesV1.java:27)
            // -> 예외가 발생해서 자원 회수 잘함
        }

        try {
            System.out.println(copyV4("resources/data.dat", "resources/dataV4.dat"));
        } catch (IOException e) {
            e.printStackTrace();
            // FileReader 생성 = io.MyFileReader@10f87f48
            // FileWriter 생성 = io.MyFileWriter2@7291c18f
            // writer close() 호출 전2
            // reader close() 호출 전
            // reader close() 호출 후
            // java.io.IOException: copyV4 .dat 파일 확장자 예외
            //     at TryWithResourcesV1.copyV4(TryWithResourcesV1.java:87)
            //     at TryWithResourcesV1.main(TryWithResourcesV1.java:43)
            //     Suppressed: java.io.IOException: writer close 호출 중 예외 발생
            //         at io.MyFileWriter2.close(MyFileWriter2.java:16)
            //         at java.base/java.io.BufferedWriter.implClose(BufferedWriter.java:398)
            //         at java.base/java.io.BufferedWriter.close(BufferedWriter.java:386)
            //         at TryWithResourcesV1.copyV4(TryWithResourcesV1.java:82)
            //         ... 1 more
            // -> 핵심 예외인 파일 확장자 예외가 잘나옴
        }
    }

    static String copyV3(String src, String dst) throws IOException {
        try (BufferedReader br = new BufferedReader(new MyFileReader(src));
             BufferedWriter bw = new BufferedWriter(new MyFileWriter(dst))) {

            // .dat 확장자면 예외를 던짐
            if (src.endsWith(".dat")) {
                throw new IOException("copyV3 .dat 파일 확장자 예외");
            }

            String line;
            while ((line = br.readLine()) != null) {
                bw.write(line);
            }
            return "ok";
        }
    }

    static String copyV4(String src, String dst) throws IOException {
        try (BufferedReader br = new BufferedReader(new MyFileReader(src));
             BufferedWriter bw = new BufferedWriter(new MyFileWriter2(dst))) {

            // .dat 확장자면 예외를 던짐
            if (src.endsWith(".dat")) {
                throw new IOException("copyV4 .dat 파일 확장자 예외");
            }

            String line;
            while ((line = br.readLine()) != null) {
                bw.write(line);
            }
            return "ok";
        }
    }
}
