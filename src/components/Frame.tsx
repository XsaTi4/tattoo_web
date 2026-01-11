import styles from './Frame.module.css';

interface FrameProps {
    children: React.ReactNode;
    className?: string;
}

export default function Frame({ children, className = '' }: FrameProps) {
    return (
        <div className={`${styles.frame} ${className}`}>
            <div className={styles.cornerTopLeft}></div>
            <div className={styles.cornerTopRight}></div>
            <div className={styles.cornerBottomLeft}></div>
            <div className={styles.cornerBottomRight}></div>
            <div className={styles.content}>
                {children}
            </div>
        </div>
    );
}
