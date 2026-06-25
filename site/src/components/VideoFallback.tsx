/**
 * VideoFallback
 *
 * HTML5-native video component with MP4/WebM fallback support.
 * Provides accessible video playback with captions, keyboard shortcuts,
 * and fallback to GIF/WebP for legacy browsers.
 *
 * Features:
 * - MP4 (H.264) primary, WebM (VP9) secondary
 * - WebVTT caption support
 * - Poster image for instant preview
 * - Full keyboard accessibility
 * - Loading state handling
 * - Fallback to static image if video unavailable
 */

import React, { useRef, useState } from 'react';

interface VideoFallbackProps {
  srcMp4: string; // MP4 video URL (H.264 codec)
  srcWebM?: string; // WebM video URL (VP9 codec)
  poster?: string; // Poster image URL
  captions?: string; // WebVTT caption file URL
  alt?: string; // Description for accessibility
  width?: number; // Video width (pixels)
  height?: number; // Video height (pixels)
  className?: string;
  autoplay?: boolean;
  loop?: boolean;
  muted?: boolean;
  controls?: boolean;
  fallbackImage?: string; // Fallback image if video unavailable
}

/**
 * HTML5 video component with MP4/WebM fallback and accessibility support.
 *
 * Renders a native HTML5 video element with:
 * - MP4 (H.264) as primary codec (widely supported)
 * - WebM (VP9) as secondary codec (better compression)
 * - WebVTT captions for accessibility
 * - Poster image for instant preview
 * - Fallback image for unsupported browsers
 *
 * Keyboard shortcuts (when focused):
 * - Space/Enter: Toggle play/pause
 * - Arrow Left: Rewind 5 seconds
 * - Arrow Right: Forward 5 seconds
 * - Arrow Up: Volume up
 * - Arrow Down: Volume down
 * - M: Toggle mute
 * - F: Toggle fullscreen
 */
export default function VideoFallback({
  srcMp4,
  srcWebM,
  poster,
  captions,
  alt,
  width,
  height,
  className = '',
  autoplay = false,
  loop = false,
  muted = false,
  controls = true,
  fallbackImage,
}: VideoFallbackProps): React.JSX.Element {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [hasError, setHasError] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  const handleError = () => {
    setHasError(true);
    setIsLoading(false);
  };

  const handleLoadStart = () => setIsLoading(true);
  const handleCanPlay = () => setIsLoading(false);

  // Focus handler for keyboard navigation
  const handleKeyDown = (e: React.KeyboardEvent<HTMLVideoElement>) => {
    const video = videoRef.current;
    if (!video) return;

    switch (e.key) {
      case ' ':
      case 'Enter':
        e.preventDefault();
        video.paused ? video.play() : video.pause();
        break;
      case 'ArrowLeft':
        e.preventDefault();
        video.currentTime = Math.max(0, video.currentTime - 5);
        break;
      case 'ArrowRight':
        e.preventDefault();
        video.currentTime = Math.min(video.duration, video.currentTime + 5);
        break;
      case 'ArrowUp':
        e.preventDefault();
        video.volume = Math.min(1, video.volume + 0.1);
        break;
      case 'ArrowDown':
        e.preventDefault();
        video.volume = Math.max(0, video.volume - 0.1);
        break;
      case 'm':
      case 'M':
        e.preventDefault();
        video.muted = !video.muted;
        break;
      case 'f':
      case 'F':
        if (document.fullscreenElement) {
          document.exitFullscreen();
        } else {
          video.requestFullscreen();
        }
        break;
    }
  };

  // Fallback to image if video unavailable
  if ((hasError || !srcMp4) && fallbackImage) {
    return (
      <img
        src={fallbackImage}
        alt={alt || 'Video unavailable'}
        width={width}
        height={height}
        className={className}
        loading="lazy"
      />
    );
  }

  return (
    <div className={`video-fallback ${className}`} role="application" aria-label={alt || 'Video player'}>
      {isLoading && <div className="video-loading" aria-hidden="true">Loading video...</div>}

      <video
        ref={videoRef}
        width={width}
        height={height}
        poster={poster}
        autoPlay={autoplay}
        loop={loop}
        muted={muted}
        controls={controls}
        onError={handleError}
        onLoadStart={handleLoadStart}
        onCanPlay={handleCanPlay}
        onKeyDown={handleKeyDown}
        aria-label={alt || 'Video'}
        className="video-element"
      >
        {/* WebM source (better compression, modern browsers) */}
        {srcWebM && <source src={srcWebM} type="video/webm" />}

        {/* MP4 source (H.264, widest support) */}
        <source src={srcMp4} type="video/mp4" />

        {/* WebVTT captions for accessibility */}
        {captions && (
          <track
            kind="captions"
            src={captions}
            srcLang="en"
            label="English Captions"
            default
          />
        )}

        {/* Fallback message for browsers without video support */}
        <div className="video-fallback-message">
          Your browser does not support HTML5 video.{' '}
          {fallbackImage && (
            <a href={fallbackImage} target="_blank" rel="noopener noreferrer">
              View static image
            </a>
          )}
        </div>
      </video>

      <style {...({'jsx': true} as any)}>{`
        .video-fallback {
          position: relative;
          display: inline-block;
        }

        .video-element {
          width: 100%;
          height: auto;
          border-radius: 4px;
          background-color: #000;
        }

        .video-loading {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          color: #fff;
          font-size: 14px;
          z-index: 1;
          pointer-events: none;
        }

        .video-fallback-message {
          padding: 20px;
          text-align: center;
          color: #000;
        }

        .video-fallback-message a {
          color: #0066cc;
          text-decoration: underline;
        }

        /* Keyboard focus indicator */
        .video-element:focus {
          outline: 2px solid #0066cc;
          outline-offset: 2px;
        }
      `}</style>
    </div>
  );
}
