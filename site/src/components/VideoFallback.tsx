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

import React, { useState } from 'react';

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
 * HTML5 video component with MP4/WebM source fallback.
 *
 * Native <video> with controls (the browser's own keyboard handling:
 * Space toggles, arrows seek/volume, M mutes, F fullscreen) plus a
 * poster for instant preview. preload="none" keeps pages light:
 * nothing is fetched until the user presses play.
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
  const [hasError, setHasError] = useState(false);

  const handleError = () => setHasError(true);

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
    <div className={`video-fallback ${className}`}>
      <video
        width={width}
        height={height}
        poster={poster}
        autoPlay={autoplay}
        loop={loop}
        muted={muted}
        controls={controls}
        // The poster (same still as above) is the preview — don't touch the
        // clip until the user presses play.
        preload="none"
        onError={handleError}
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
    </div>
  );
}
