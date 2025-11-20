package date;

import java.util.Date;

public final class Period {
    private final Date start;
    private final Date end;

    public Period(Date start, Date end) {
        this.start = start;
        this.end = end;
    }

    public long getDateDiff() {
        return end.getTime() - start.getTime();
    }
}
