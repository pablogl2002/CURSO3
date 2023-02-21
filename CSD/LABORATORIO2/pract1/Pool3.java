// CSD feb 2015 Juansa Sendra

public class Pool3 extends Pool{ //max capacity
    int nInst = 0;
    int nKids = 0;
    int mki = 2;
    int capM = 5;
    
    
    public void init(int ki, int cap)           {
        mki = ki;
        capM = cap;
    }
    public synchronized void kidSwims() throws InterruptedException {
        while (nInst <= 0 || nKids >= mki * nInst || capM == nInst + nKids) {
            log.waitingToSwim();
            wait();
        }
        nKids++;
        notifyAll();
        log.swimming();
    }
    public synchronized void kidRests()      {
        nKids--;
        log.resting();
        notifyAll();
    }
    public synchronized void instructorSwims() throws InterruptedException {
        while (capM == nInst + nKids) {
            log.waitingToSwim();
            wait();
        }
        nInst++;
        log.swimming();
        notifyAll();
    }
    public synchronized void instructorRests() throws InterruptedException {
        while (nKids > mki * (nInst - 1) && nInst > 0) {
            log.waitingToRest();
            wait();
        }
        nInst--;
        log.resting();
        notifyAll();
    }
}
